import os
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
from supabase_client import get_supabase_client
try:
    from global_catalog import CATALOG_BY_TICKER
    COMPANY_FULL_NAMES = {k: v["company_name"] for k, v in CATALOG_BY_TICKER.items()}
except ImportError:
    COMPANY_FULL_NAMES = {
        "AAPL": "Apple Inc.",
        "NVDA": "NVIDIA Corporation",
        "TSLA": "Tesla, Inc.",
        "MSFT": "Microsoft Corporation",
        "AMZN": "Amazon.com, Inc.",
        "GOOGL": "Alphabet Inc.",
        "META": "Meta Platforms, Inc.",
        "TCS.NS": "Tata Consultancy Services",
        "INFY.NS": "Infosys Limited",
        "SAP.DE": "SAP SE",
        "7203.T": "Toyota Motor Corporation",
        "BHP.AX": "BHP Group Limited",
        "SHOP.TO": "Shopify Inc."
    }

def normalize_ticker(ticker: str) -> str:
    """Normalizes the ticker symbol."""
    return (ticker or "").strip().upper()

def is_cache_sufficient(client, ticker: str, req_start_date: str, req_end_date: str, years: int) -> bool:
    """
    Checks whether Supabase stock_prices contains sufficient data
    to cover the requested analysis period for the ticker.
    """
    try:
        # Check earliest trading date in cache
        min_res = client.table("stock_prices") \
            .select("trading_date") \
            .eq("ticker", ticker) \
            .order("trading_date", desc=False) \
            .limit(1) \
            .execute()
        if not min_res.data:
            return False

        # Check latest trading date in cache
        max_res = client.table("stock_prices") \
            .select("trading_date") \
            .eq("ticker", ticker) \
            .order("trading_date", desc=True) \
            .limit(1) \
            .execute()
        if not max_res.data:
            return False

        earliest_cached = min_res.data[0]["trading_date"]
        latest_cached = max_res.data[0]["trading_date"]

        now = datetime.now()
        # Market data should be recent (within last 4 calendar days accounting for weekends/holidays)
        recent_threshold = (now - timedelta(days=4)).strftime('%Y-%m-%d')

        # Earliest date must be <= requested start date (or within 7 days of start date)
        start_threshold = (datetime.strptime(req_start_date, '%Y-%m-%d') + timedelta(days=7)).strftime('%Y-%m-%d')

        if earliest_cached > start_threshold:
            return False

        if latest_cached < recent_threshold:
            return False

        return True
    except Exception as e:
        # Safe logging without exposing secrets
        print(f"Error checking cache sufficiency for {ticker}: {type(e).__name__}", flush=True)
        return False

def get_cached_stock_data(client, ticker: str, req_start_date: str, req_end_date: str) -> pd.DataFrame | None:
    """
    Retrieves cached stock prices from Supabase and formats them as a DataFrame.
    Paginates to support multi-year datasets (>1000 rows).
    """
    try:
        all_rows = []
        step = 1000
        offset = 0

        while True:
            res = client.table("stock_prices") \
                .select("trading_date, open, high, low, close, adjusted_close, volume") \
                .eq("ticker", ticker) \
                .gte("trading_date", req_start_date) \
                .lte("trading_date", req_end_date) \
                .order("trading_date", desc=False) \
                .range(offset, offset + step - 1) \
                .execute()

            rows = res.data or []
            all_rows.extend(rows)
            if len(rows) < step:
                break
            offset += step

        if not all_rows:
            return None

        df = pd.DataFrame(all_rows)
        df['Date'] = pd.to_datetime(df['trading_date'])
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)

        # Standardize column names for analysis engine
        col_map = {
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'adjusted_close': 'Adj Close',
            'volume': 'Volume'
        }
        for src_col, target_col in col_map.items():
            if src_col in df.columns:
                df[target_col] = pd.to_numeric(df[src_col], errors='coerce')

        if 'Close' not in df.columns or df['Close'].dropna().empty:
            return None

        # Drop rows where Close is null
        df = df.dropna(subset=['Close'])
        return df

    except Exception as e:
        print(f"Error reading stock_prices cache for {ticker}: {type(e).__name__}", flush=True)
        return None

def save_stock_data_to_supabase(client, ticker: str, hist: pd.DataFrame, stock_obj=None) -> bool:
    """
    Saves historical price records into Supabase stock_prices table in batches,
    and updates the companies table with company info.
    """
    if hist is None or hist.empty:
        return False

    try:
        records = []
        for idx, row in hist.iterrows():
            if hasattr(idx, 'strftime'):
                trading_date = idx.strftime('%Y-%m-%d')
            else:
                trading_date = str(idx)[:10]

            open_val = float(row['Open']) if 'Open' in row and pd.notna(row['Open']) else None
            high_val = float(row['High']) if 'High' in row and pd.notna(row['High']) else None
            low_val = float(row['Low']) if 'Low' in row and pd.notna(row['Low']) else None
            close_val = float(row['Close']) if 'Close' in row and pd.notna(row['Close']) else None
            adj_val = float(row['Adj Close']) if 'Adj Close' in row and pd.notna(row['Adj Close']) else close_val
            vol_val = int(row['Volume']) if 'Volume' in row and pd.notna(row['Volume']) else None

            records.append({
                "ticker": ticker,
                "trading_date": trading_date,
                "open": round(open_val, 4) if open_val is not None else None,
                "high": round(high_val, 4) if high_val is not None else None,
                "low": round(low_val, 4) if low_val is not None else None,
                "close": round(close_val, 4) if close_val is not None else None,
                "adjusted_close": round(adj_val, 4) if adj_val is not None else None,
                "volume": vol_val
            })

        # Upsert stock prices in batches of 500
        batch_size = 500
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            client.table("stock_prices").upsert(batch, on_conflict="ticker,trading_date").execute()

        print(f"Successfully saved {len(records)} records for {ticker} into Supabase stock_prices.", flush=True)

        # Update company metadata in companies table
        try:
            company_name = COMPANY_FULL_NAMES.get(ticker, f"{ticker} Inc.")
            exchange = "NASDAQ"
            country = "United States"

            if stock_obj is not None:
                try:
                    info = getattr(stock_obj, 'fast_info', None)
                    if info and hasattr(info, 'exchange'):
                        exchange = info.exchange or exchange
                    full_info = getattr(stock_obj, 'info', {}) or {}
                    company_name = full_info.get("longName") or full_info.get("shortName") or company_name
                    exchange = full_info.get("exchange") or exchange
                    country = full_info.get("country") or country
                except Exception:
                    pass

            client.table("companies").upsert({
                "ticker": ticker,
                "company_name": company_name,
                "exchange": exchange,
                "country": country
            }, on_conflict="ticker").execute()
        except Exception as ce:
            print(f"Notice: Company metadata update skipped: {type(ce).__name__}", flush=True)

        return True

    except Exception as e:
        print(f"Error saving stock_prices to Supabase for {ticker}: {type(e).__name__}", flush=True)
        return False

def get_stock_data(ticker: str, years: int) -> tuple[pd.DataFrame, str]:
    """
    Main retrieval function:
    1. Normalizes ticker.
    2. Checks Supabase stock_prices cache.
    3. If sufficient, returns cached DataFrame with data_source='supabase_cache'.
    4. If missing/incomplete, fetches from yfinance, saves to Supabase, returns data_source='yfinance'.
    """
    ticker = normalize_ticker(ticker)
    now = datetime.now()
    req_start_date = (now - timedelta(days=int(years * 365.25))).strftime('%Y-%m-%d')
    req_end_date = (now + timedelta(days=1)).strftime('%Y-%m-%d')

    client = None
    try:
        client = get_supabase_client()
    except Exception as e:
        print(f"Notice: Supabase client unavailable: {type(e).__name__}", flush=True)

    # 1. Try cache if client available
    if client is not None:
        if is_cache_sufficient(client, ticker, req_start_date, req_end_date, years):
            cached_df = get_cached_stock_data(client, ticker, req_start_date, req_end_date)
            if cached_df is not None and not cached_df.empty:
                print(f"Using cached data for {ticker}", flush=True)
                return cached_df, "supabase_cache"

    # 2. Fetch missing data from yfinance
    print(f"Fetching missing data for {ticker} from yfinance", flush=True)
    stock = yf.Ticker(ticker)
    hist = pd.DataFrame()
    try:
        hist = stock.history(start=req_start_date, end=req_end_date, interval="1d", auto_adjust=True)
    except Exception:
        pass

    if hist is None or hist.empty:
        try:
            hist = stock.history(period=f"{years}y", interval="1d", auto_adjust=True)
        except Exception:
            pass

    if hist is None or hist.empty:
        raise ValueError(f"No historical data found for {ticker}")

    # Ensure timezone naive
    if hist.index.tz is not None:
        hist.index = hist.index.tz_localize(None)

    # 3. Save newly downloaded records to Supabase
    if client is not None:
        save_stock_data_to_supabase(client, ticker, hist, stock)

    return hist, "yfinance"
