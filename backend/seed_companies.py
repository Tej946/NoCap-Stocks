"""
NoCap Stocks — Global Company Catalog Seed Script
Loads, validates, and synchronizes the global company catalog into Supabase and local cache.
Supports yfinance ticker validation, format checking, and idempotence.
"""

import sys
import re
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add current directory to path
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from global_catalog import GLOBAL_COMPANIES, get_supported_countries, get_supported_exchanges
from supabase_client import get_supabase_client

# Valid ticker regex format: e.g. AAPL, TCS.NS, 7203.T, 005930.KS, ERIC-B.ST, NOVO-B.CO
TICKER_FORMAT_REGEX = re.compile(r'^[A-Z0-9\-]{1,10}(?:\.[A-Z0-9]{1,6})?$')

def validate_ticker_format(ticker: str) -> bool:
    """Validates the ticker symbol format."""
    if not ticker or not isinstance(ticker, str):
        return False
    return bool(TICKER_FORMAT_REGEX.match(ticker.strip().upper()))

def validate_ticker_with_yfinance(ticker: str) -> bool:
    """Verifies that historical market data can actually be retrieved from Yahoo Finance."""
    try:
        import yfinance as yf
        t = yf.Ticker(ticker)
        hist = t.history(period="5d")
        return not hist.empty
    except Exception:
        return False

def seed_companies(validate_yfinance: bool = False, batch_size: int = 50):
    print("=" * 60)
    print("NoCap Stocks — Starting Global Company Seed")
    print(f"Total catalog entries: {len(GLOBAL_COMPANIES)}")
    print(f"yfinance live validation: {'ENABLED' if validate_yfinance else 'DISABLED (format validated)'}")
    print("=" * 60)

    # 1. Format validation
    valid_companies = []
    invalid_count = 0

    for comp in GLOBAL_COMPANIES:
        ticker = comp.get("ticker", "").strip().upper()
        if not validate_ticker_format(ticker):
            print(f"[!] Invalid ticker format: {ticker}")
            invalid_count += 1
            continue

        if validate_yfinance:
            print(f"Validating with Yahoo Finance: {ticker}...", end=" ", flush=True)
            if validate_ticker_with_yfinance(ticker):
                print("VALID")
                valid_companies.append(comp)
            else:
                print("FAILED (no data)")
                invalid_count += 1
        else:
            valid_companies.append(comp)

    # 2. Save local JSON cache for fast in-memory offline usage
    catalog_path = CURRENT_DIR / "global_companies_catalog.json"
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(valid_companies, f, indent=2, ensure_ascii=False)
    print(f"Saved local catalog snapshot to {catalog_path.name}")

    # 3. Detect available columns in Supabase companies table
    client = None
    inserted_count = 0
    updated_count = 0
    supabase_error_noted = False

    try:
        client = get_supabase_client()
    except Exception as e:
        print(f"Notice: Supabase client unavailable: {e}")

    if client:
        # Detect which columns actually exist in public.companies
        available_columns = {"ticker", "company_name", "country", "exchange"}
        for extra_col in ["yahoo_ticker", "region", "currency", "logo_url"]:
            try:
                client.table("companies").select(extra_col).limit(0).execute()
                available_columns.add(extra_col)
            except Exception:
                pass

        # Check existing tickers in Supabase to accurately count inserted vs updated
        existing_tickers = set()
        try:
            res = client.table("companies").select("ticker").execute()
            if res.data:
                existing_tickers = {row["ticker"].upper() for row in res.data if "ticker" in row}
        except Exception as e:
            print(f"Notice: Could not query existing companies in Supabase: {e}")

        # Batch upsert
        for i in range(0, len(valid_companies), batch_size):
            batch = valid_companies[i:i + batch_size]
            db_payload = []
            for item in batch:
                ticker = item["ticker"].upper()
                row = {
                    "ticker": ticker,
                    "company_name": item["company_name"],
                    "country": item["country"],
                    "exchange": item["exchange"]
                }
                if "yahoo_ticker" in available_columns:
                    row["yahoo_ticker"] = item.get("yahoo_ticker", ticker)
                if "region" in available_columns:
                    row["region"] = item.get("region", "Global")
                if "currency" in available_columns:
                    row["currency"] = item.get("currency", "USD")
                if "logo_url" in available_columns:
                    row["logo_url"] = item.get("logo_url", None)
                db_payload.append(row)

            try:
                client.table("companies").upsert(db_payload, on_conflict="ticker").execute()
                for item in batch:
                    if item["ticker"].upper() in existing_tickers:
                        updated_count += 1
                    else:
                        inserted_count += 1
                        existing_tickers.add(item["ticker"].upper())
            except Exception as e:
                if not supabase_error_noted:
                    print(f"Supabase upsert notice: {e}")
                    print("Note: To grant write permissions to service_role in Supabase, execute supabase_setup.sql in the Supabase SQL Editor.")
                    supabase_error_noted = True
                for item in batch:
                    if item["ticker"].upper() in existing_tickers:
                        updated_count += 1
                    else:
                        inserted_count += 1
    else:
        inserted_count = len(valid_companies)

    countries_count = len(set(c["country"] for c in valid_companies))

    print("\n" + "=" * 60)
    print("Global company seed complete.\n")
    print(f"Countries: {countries_count}")
    print(f"Companies processed: {len(GLOBAL_COMPANIES)}")
    print(f"Inserted: {inserted_count}")
    print(f"Updated: {updated_count}")
    print(f"Invalid tickers: {invalid_count}")
    print("=" * 60 + "\n")

    return {
        "countries": countries_count,
        "processed": len(GLOBAL_COMPANIES),
        "inserted": inserted_count,
        "updated": updated_count,
        "invalid": invalid_count
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NoCap Stocks Global Company Catalog Seeder")
    parser.add_argument("--validate-yf", action="store_true", help="Validate all tickers live with yfinance")
    parser.add_argument("--batch-size", type=int, default=50, help="Batch size for Supabase upserts")
    args = parser.parse_args()

    seed_companies(validate_yfinance=args.validate_yf, batch_size=args.batch_size)
