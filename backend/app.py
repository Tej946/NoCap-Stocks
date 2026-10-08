import os
import re
import math
import urllib.request
import urllib.parse
import json
from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf
from analysis import analyze_stock_drops
from supabase_client import get_supabase_client
from global_catalog import (
    GLOBAL_COMPANIES,
    CATALOG_BY_TICKER,
    COMPANY_ALIAS_MAP,
    get_all_companies,
    get_company_by_ticker,
    get_supported_countries,
    get_supported_exchanges
)

# Load environment variables from .env
try:
    from dotenv import load_dotenv
    root_env = Path(__file__).resolve().parent.parent / '.env'
    backend_env = Path(__file__).resolve().parent / '.env'
    if root_env.exists():
        load_dotenv(dotenv_path=root_env)
    if backend_env.exists():
        load_dotenv(dotenv_path=backend_env)
except ImportError:
    pass

app = Flask(__name__)

# -----------------------------------------------------------------------
# CORS Configuration
# Allowed origins for NoCap Stocks:
# - Production frontend: https://nocap-stocks.onrender.com
# - Local development frontends: localhost and 127.0.0.1 on ports 3000, 5000, 5500, 8000
# - Plus any origins explicitly specified in CORS_ORIGINS env var.
# NOTE: Wildcard "*" is never used as the permanent production origin.
# -----------------------------------------------------------------------
_DEFAULT_CORS_ORIGINS = [
    "https://nocap-stocks.onrender.com",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://127.0.0.1:5000",
    "http://localhost:5000",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

_cors_origins = list(_DEFAULT_CORS_ORIGINS)
_env_cors = os.environ.get("CORS_ORIGINS", "").strip()
if _env_cors and _env_cors != "*":
    for _o in _env_cors.split(","):
        _clean = _o.strip().rstrip("/")
        if _clean and _clean not in _cors_origins:
            _cors_origins.append(_clean)

def is_allowed_origin(origin: str | None) -> bool:
    if not origin:
        return False
    o_norm = origin.strip().rstrip("/").lower()
    return any(o_norm == a.rstrip("/").lower() for a in _cors_origins)

CORS(
    app,
    resources={
        r"/*": {
            "origins": _cors_origins,
            "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Accept", "Authorization", "X-Requested-With"],
            "supports_credentials": False,
            "max_age": 86400,
        }
    },
)

@app.before_request
def handle_preflight():
    """Handle CORS OPTIONS preflight explicitly to guarantee successful 200 response."""
    if request.method == "OPTIONS":
        origin = request.headers.get("Origin")
        if is_allowed_origin(origin):
            res = app.make_default_options_response()
            res.headers["Access-Control-Allow-Origin"] = origin
            res.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
            res.headers["Access-Control-Allow-Headers"] = "Content-Type, Accept, Authorization, X-Requested-With"
            res.headers["Access-Control-Max-Age"] = "86400"
            return res

@app.after_request
def add_cors_headers(response):
    """Ensure CORS headers are present on all responses if requested by an allowed origin."""
    origin = request.headers.get("Origin")
    if is_allowed_origin(origin):
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Accept, Authorization, X-Requested-With"
        response.headers["Access-Control-Max-Age"] = "86400"
    return response

# Guaranteed CORS headers on all HTTP error status codes (400, 401, 403, 404, 429, 500)
@app.errorhandler(400)
def handle_bad_request(e):
    return add_cors_headers(jsonify({"error": "Bad request", "message": str(e)})), 400

@app.errorhandler(401)
def handle_unauthorized(e):
    return add_cors_headers(jsonify({"error": "Unauthorized", "message": str(e)})), 401

@app.errorhandler(403)
def handle_forbidden(e):
    return add_cors_headers(jsonify({"error": "Forbidden", "message": str(e)})), 403

@app.errorhandler(404)
def handle_not_found(e):
    return add_cors_headers(jsonify({"error": "Not found", "message": str(e)})), 404

@app.errorhandler(429)
def handle_rate_limit(e):
    return add_cors_headers(jsonify({"error": "Too many requests", "message": str(e)})), 429

@app.errorhandler(500)
def handle_internal_error(e):
    return add_cors_headers(jsonify({"error": "Internal server error", "message": str(e)})), 500

@app.errorhandler(Exception)
def handle_general_exception(e):
    print(f"[SERVER ERROR] {type(e).__name__}: {str(e)}", flush=True)
    return add_cors_headers(jsonify({"error": "Internal server error", "message": str(e)})), 500

def sanitize_json_value(obj):
    """
    Recursively converts unsupported values for strict valid JSON:
    - NaN, Inf, -Inf -> None (never replaced with fake zeroes)
    - numpy scalars -> native int / float
    - numpy ndarray -> python list
    - pandas Timestamp / datetime / date -> ISO string
    - pandas NaT -> None
    - dict -> recursively sanitized dict with str keys
    - list / tuple / set -> recursively sanitized list
    """
    if obj is None:
        return None
    if isinstance(obj, (float, np.floating)):
        if math.isnan(obj) or np.isnan(obj):
            return None
        if math.isinf(obj) or np.isinf(obj):
            return None
        return float(obj)
    if isinstance(obj, (bool, np.bool_)):
        return bool(obj)
    if isinstance(obj, (int, np.integer)):
        return int(obj)
    if isinstance(obj, (pd.Timestamp, datetime)):
        if pd.isna(obj):
            return None
        return obj.isoformat()
    if hasattr(pd, "NaT") and obj is pd.NaT:
        return None
    if isinstance(obj, np.ndarray):
        return [sanitize_json_value(x) for x in obj.tolist()]
    if isinstance(obj, dict):
        return {str(k): sanitize_json_value(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [sanitize_json_value(x) for x in obj]
    if isinstance(obj, str):
        return obj
    try:
        if pd.isna(obj):
            return None
    except Exception:
        pass
    return str(obj)


# Build Company Metadata dictionary from Global Catalog
COMPANY_METADATA = {}
for comp in GLOBAL_COMPANIES:
    COMPANY_METADATA[comp["ticker"].upper()] = {
        "name": comp["company_name"],
        "exchange": comp["exchange"],
        "country": comp["country"],
        "yahoo_ticker": comp.get("yahoo_ticker", comp["ticker"]),
        "currency": comp.get("currency", "USD"),
        "region": comp.get("region", "Global")
    }

# Build Alias / Ticker Search Map from Global Catalog and Aliases
COMPANY_TICKER_MAP = dict(COMPANY_ALIAS_MAP)
for comp in GLOBAL_COMPANIES:
    t = comp["ticker"].upper()
    COMPANY_TICKER_MAP[comp["ticker"].lower()] = t
    COMPANY_TICKER_MAP[comp["company_name"].lower()] = t
    # Also index without exchange suffix (e.g. "tcs" -> "TCS.NS")
    if "." in t:
        base = t.split(".")[0].lower()
        if base not in COMPANY_TICKER_MAP:
            COMPANY_TICKER_MAP[base] = t

COMPANY_FULL_NAMES = {k: v["name"] for k, v in COMPANY_METADATA.items()}

# In-memory fast cache for company prices & metadata (TTL: 5 mins)
_MARKET_CACHE = {}

_DEFAULT_WATCHLIST_SNAPSHOT = {
    "AAPL": {"latest_price": 227.63, "previous_close": 226.70, "daily_change_pct": 0.41},
    "MSFT": {"latest_price": 430.30, "previous_close": 431.25, "daily_change_pct": -0.22},
    "NVDA": {"latest_price": 121.40, "previous_close": 119.51, "daily_change_pct": 1.58},
    "TSLA": {"latest_price": 261.63, "previous_close": 255.37, "daily_change_pct": 2.45},
    "AMZN": {"latest_price": 186.40, "previous_close": 184.83, "daily_change_pct": 0.85},
    "GOOGL": {"latest_price": 165.85, "previous_close": 166.42, "daily_change_pct": -0.34},
    "META": {"latest_price": 567.36, "previous_close": 562.19, "daily_change_pct": 0.92},
    "TCS.NS": {"latest_price": 4260.00, "previous_close": 4232.50, "daily_change_pct": 0.65},
    "INFY.NS": {"latest_price": 1895.50, "previous_close": 1874.50, "daily_change_pct": 1.12},
    "RELIANCE.NS": {"latest_price": 2950.00, "previous_close": 2926.60, "daily_change_pct": 0.80},
    "SAP.DE": {"latest_price": 204.10, "previous_close": 202.60, "daily_change_pct": 0.74},
    "7203.T": {"latest_price": 2610.00, "previous_close": 2621.80, "daily_change_pct": -0.45},
    "005930.KS": {"latest_price": 74200.00, "previous_close": 73280.00, "daily_change_pct": 1.25},
    "0700.HK": {"latest_price": 375.40, "previous_close": 371.87, "daily_change_pct": 0.95},
    "ASML.AS": {"latest_price": 785.20, "previous_close": 791.53, "daily_change_pct": -0.80},
    "SHOP.TO": {"latest_price": 104.25, "previous_close": 102.33, "daily_change_pct": 1.88},
    "BHP.AX": {"latest_price": 44.82, "previous_close": 44.68, "daily_change_pct": 0.32},
    "2330.TW": {"latest_price": 975.00, "previous_close": 955.00, "daily_change_pct": 2.10}
}

def get_stakes_emoji(stakes: str) -> str:
    s = (stakes or "").upper()
    if s == "HIGH":
        return "🔴"
    elif s == "MODERATE":
        return "🟡"
    elif s == "LOW":
        return "🟢"
    else:
        return "⚪"

def clean_extracted_query(text: str) -> str:
    cleaned = (text or "").strip()
    cleaned = re.sub(
        r'^(?:can you\s+)?(?:please\s+)?(?:explain|explain what happened to|explain what happened historically after|what happened to|what happened after|show me historical behavior of|analyze|analysis of|check out|check|look at|tell me about|what about|how about|i asked for|i asked|i aswd|i want|research|evaluate|investigate|give me info on|give me|show me|search for|search|pull up)\s+',
        '',
        cleaned,
        flags=re.IGNORECASE
    )
    cleaned = re.sub(r'^(?:i\s+[a-z]{1,8}\s+)', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(
        r'\s+(?:shares|share|stock|stocks|equity|securities|historical drops|had large historical drops|drops|behavior|historical behavior)\b.*$',
        '',
        cleaned,
        flags=re.IGNORECASE
    )
    return cleaned.strip(" !?,.:;\"'")

import unicodedata

def normalize_for_search(text: str) -> str:
    if not text:
        return ""
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[\s\W_]+', '', text)
    return text.lower()

def search_companies(query: str) -> list:
    """
    Global search returning matches:
    Search priority:
    1. Exact ticker match
    2. Exact company name
    3. Global Catalog / Supabase matches (prefix or substring)
    4. Yahoo Finance quote search for unseeded global equities
    5. Deduplication and ranking
    """
    if not query:
        return []
    q_clean = query.strip()
    q_lower = q_clean.lower()
    q_upper = q_clean.upper()
    q_norm = normalize_for_search(query)
    matches = []
    seen = set()

    # 1. Exact ticker match in catalog
    if q_upper in CATALOG_BY_TICKER:
        c = CATALOG_BY_TICKER[q_upper]
        matches.append({
            "ticker": c["ticker"],
            "company_name": c["company_name"],
            "exchange": c["exchange"],
            "country": c["country"]
        })
        seen.add(c["ticker"].upper())

    # 2. Exact match in alias map
    if q_lower in COMPANY_TICKER_MAP:
        sym = COMPANY_TICKER_MAP[q_lower]
        if sym not in seen and sym in CATALOG_BY_TICKER:
            c = CATALOG_BY_TICKER[sym]
            matches.append({
                "ticker": c["ticker"],
                "company_name": c["company_name"],
                "exchange": c["exchange"],
                "country": c["country"]
            })
            seen.add(sym)

    # 3. Catalog matching: prefix matches first, then substring
    prefix_matches = []
    sub_matches = []
    for c in GLOBAL_COMPANIES:
        sym = c["ticker"].upper()
        if sym in seen:
            continue
            
        sym_norm = normalize_for_search(sym)
        name_norm = normalize_for_search(c["company_name"])
        
        if sym_norm.startswith(q_norm) or name_norm.startswith(q_norm):
            prefix_matches.append({
                "ticker": c["ticker"],
                "company_name": c["company_name"],
                "exchange": c["exchange"],
                "country": c["country"]
            })
            seen.add(sym)
        elif q_norm in sym_norm or q_norm in name_norm:
            sub_matches.append({
                "ticker": c["ticker"],
                "company_name": c["company_name"],
                "exchange": c["exchange"],
                "country": c["country"]
            })
            seen.add(sym)

    matches.extend(prefix_matches)
    matches.extend(sub_matches)

    # 4. If query length >= 2, query Yahoo Finance search endpoint
    if len(q_clean) >= 2 and len(matches) < 8:
        try:
            url = f"https://query2.finance.yahoo.com/v1/finance/search?q={urllib.parse.quote(q_clean)}&quotesCount=8&newsCount=0&enableFuzzyQuery=false"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                quotes = data.get('quotes', [])
                for q in quotes:
                    sym = q.get('symbol')
                    qtype = q.get('quoteType', '')
                    if sym and qtype in ['EQUITY', 'ETF'] and sym.upper() not in seen:
                        seen.add(sym.upper())
                        matches.append({
                            "ticker": sym,
                            "company_name": q.get('shortname') or q.get('longname') or sym,
                            "exchange": q.get('exchange', 'GLOBAL'),
                            "country": ""
                        })
        except Exception as e:
            print(f"Notice: Yahoo Finance quote search error: {e}", flush=True)

    return matches[:15]

CONVERSATIONAL_WORDS = {
    "hello", "hi", "hey", "hola", "greetings", "good morning", "good afternoon",
    "good evening", "howdy", "sup", "yo", "help", "who are you", "what can you do",
    "what is this", "how does this work", "thanks", "thank you", "bye", "goodbye"
}

FINANCIAL_METRIC_TERMS = {
    "volatility", "win rate", "drop threshold", "window days", "drawdown",
    "historical stakes", "median return", "average return", "standard deviation",
    "candlestick", "volume", "market cap", "drops", "drop event"
}

def resolve_company_to_ticker(query: str) -> dict:
    """
    Robust Company/Ticker Resolver:
    1. Cleans conversational prefixes and suffixes.
    2. Identifies conversational greetings or pure financial metric questions.
    3. Searches catalog, exact ticker match, exact alias map.
    4. Validates formatted tickers with yfinance.
    5. Searches Yahoo Finance quote endpoint.
    NEVER silently falls back to AAPL.
    If company cannot be resolved, returns:
    {
        "resolved": False,
        "results": [],
        "message": "No matching company found."
    }
    """
    if not query or not query.strip():
        return {
            "resolved": False,
            "results": [],
            "message": "No matching company found.",
            "extracted": ""
        }

    extracted = clean_extracted_query(query)
    if not extracted:
        return {
            "resolved": False,
            "results": [],
            "message": "No matching company found.",
            "extracted": ""
        }

    ext_lower = extracted.lower()
    ext_upper = extracted.upper()

    # Conversational greeting check (e.g. "hello", "hi", "help")
    if ext_lower in CONVERSATIONAL_WORDS:
        return {
            "resolved": False,
            "ticker": None,
            "company_name": None,
            "exchange": None,
            "country": None,
            "results": [],
            "message": "Conversational input.",
            "extracted": extracted,
            "is_conversational": True
        }

    # Financial metric check (e.g. "volatility", "win rate")
    if ext_lower in FINANCIAL_METRIC_TERMS:
        return {
            "resolved": False,
            "ticker": None,
            "company_name": None,
            "exchange": None,
            "country": None,
            "results": [],
            "message": "Financial metric inquiry.",
            "extracted": extracted,
            "is_metric": True
        }

    # 1. Exact ticker in catalog
    if ext_upper in CATALOG_BY_TICKER:
        c = CATALOG_BY_TICKER[ext_upper]
        return {
            "resolved": True,
            "ticker": c["ticker"],
            "company_name": c["company_name"],
            "exchange": c["exchange"],
            "country": c["country"],
            "results": [c],
            "extracted": extracted
        }

    # 2. Exact match in alias map
    if ext_lower in COMPANY_TICKER_MAP:
        sym = COMPANY_TICKER_MAP[ext_lower]
        c = CATALOG_BY_TICKER.get(sym, {
            "ticker": sym,
            "company_name": COMPANY_FULL_NAMES.get(sym, sym),
            "exchange": "GLOBAL",
            "country": ""
        })
        return {
            "resolved": True,
            "ticker": sym,
            "company_name": c["company_name"],
            "exchange": c.get("exchange", "GLOBAL"),
            "country": c.get("country", ""),
            "results": [c],
            "extracted": extracted
        }

    # 3. Direct ticker format check (e.g. MSFT, TCS.NS, 7203.T, 005930.KS, ERIC-B.ST)
    if re.match(r'^[A-Z0-9\-]{1,10}(?:\.[A-Z0-9]{1,6})?$', ext_upper):
        try:
            tkr = yf.Ticker(ext_upper)
            hist = tkr.history(period="5d")
            if not hist.empty:
                fast = getattr(tkr, 'fast_info', None)
                name = COMPANY_FULL_NAMES.get(ext_upper)
                if not name and fast and hasattr(fast, 'shortName'):
                    name = fast.shortName
                if not name:
                    try:
                        info = getattr(tkr, 'info', {}) or {}
                        name = info.get("longName") or info.get("shortName") or ext_upper
                    except Exception:
                        name = ext_upper
                exch = getattr(fast, 'exchange', "GLOBAL") if fast else "GLOBAL"
                res_obj = {
                    "ticker": ext_upper,
                    "company_name": name,
                    "exchange": exch,
                    "country": ""
                }
                return {
                    "resolved": True,
                    "ticker": ext_upper,
                    "company_name": name,
                    "exchange": exch,
                    "country": "",
                    "results": [res_obj],
                    "extracted": extracted
                }
        except Exception:
            pass

    # 4. Search via search_companies (Catalog + Yahoo)
    search_results = search_companies(extracted)
    if search_results:
        # Check if user specifically asked for "Samsung", "Toyota", "Puma" etc.
        primary = search_results[0]
        # Puma preference check
        if ext_lower == "puma":
            for r in search_results:
                if r["ticker"] in ["PUM.DE", "PUMSY"]:
                    primary = r
                    break
        # Samsung preference check
        elif ext_lower == "samsung":
            for r in search_results:
                if r["ticker"] == "005930.KS":
                    primary = r
                    break

        return {
            "resolved": True,
            "ticker": primary["ticker"],
            "company_name": primary["company_name"],
            "exchange": primary["exchange"],
            "country": primary["country"],
            "results": search_results,
            "extracted": extracted
        }

    # 5. Absolutely No Fallback to AAPL
    return {
        "resolved": False,
        "results": [],
        "message": "No matching company found.",
        "extracted": extracted
    }

def get_company_info(ticker: str) -> dict | None:
    """
    Retrieves company metadata, latest historical price, previous close, and % change.
    Never silently falls back to AAPL.
    """
    if not ticker or not isinstance(ticker, str) or not ticker.strip():
        return None

    ticker = ticker.strip().upper()
    now_ts = datetime.now().timestamp()

    # Check cache (120s TTL)
    if ticker in _MARKET_CACHE and (now_ts - _MARKET_CACHE[ticker]["ts"]) < 120:
        return _MARKET_CACHE[ticker]["data"]

    catalog_entry = CATALOG_BY_TICKER.get(ticker)
    meta = COMPANY_METADATA.get(ticker, {
        "name": catalog_entry["company_name"] if catalog_entry else f"{ticker}",
        "exchange": catalog_entry["exchange"] if catalog_entry else "GLOBAL",
        "country": catalog_entry["country"] if catalog_entry else "Global"
    })

    last_price = None
    prev_close = None
    latest_date = datetime.now().strftime('%Y-%m-%d')
    company_name = meta["name"]
    exchange = meta.get("exchange", "GLOBAL")
    country = meta.get("country", "")

    try:
        t = yf.Ticker(ticker)
        fast = getattr(t, 'fast_info', None)
        if fast:
            last_price = getattr(fast, 'last_price', None)
            prev_close = getattr(fast, 'previous_close', None)
            if hasattr(fast, 'exchange') and fast.exchange:
                exchange = fast.exchange

        if last_price is None or prev_close is None:
            hist = t.history(period="5d")
            if not hist.empty:
                last_price = float(hist['Close'].iloc[-1])
                prev_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else last_price
                latest_date = hist.index[-1].strftime('%Y-%m-%d')
        else:
            hist = t.history(period="5d")
            if not hist.empty:
                latest_date = hist.index[-1].strftime('%Y-%m-%d')

        if company_name == ticker and hasattr(t, 'info') and t.info:
            company_name = t.info.get("longName") or t.info.get("shortName") or company_name
            country = t.info.get("country") or country
    except Exception as e:
        print(f"Notice: Error fetching price info for {ticker}: {e}", flush=True)

    chg_pct = 0.0
    if last_price is not None and prev_close and prev_close > 0:
        chg_pct = round(((last_price - prev_close) / prev_close) * 100, 2)

    result = {
        "ticker": ticker,
        "company_name": company_name,
        "exchange": exchange,
        "country": country,
        "latest_price": round(float(last_price), 2) if last_price is not None else None,
        "previous_close": round(float(prev_close), 2) if prev_close is not None else None,
        "daily_change_pct": chg_pct,
        "latest_available_date": latest_date
    }

    _MARKET_CACHE[ticker] = {"data": result, "ts": now_ts}
    return result

# ==============================================================================
# REST API ENDPOINTS
# ==============================================================================

@app.route("/")
def home():
    return jsonify({
        "message": "NoCap Stocks Global Platform Backend is running!",
        "version": "3.0.0",
        "tagline": "No fake predictions. Just historical data.",
        "coverage": "Global companies supported by available Yahoo Finance market coverage.",
        "supported_countries_count": len(get_supported_countries()),
        "supported_companies_count": len(GLOBAL_COMPANIES)
    })

@app.route("/health")
@app.route("/api/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "nocap-stocks-backend",
        "timestamp": datetime.utcnow().isoformat()
    }), 200

@app.route("/api/supabase/test", methods=["GET"])
def test_supabase_connection():
    try:
        client = get_supabase_client()
        if not client:
            return jsonify({
                "connected": False,
                "message": "Supabase client not initialized (missing environment variables)."
            }), 200
        try:
            client.table("companies").select("*").limit(1).execute()
            return jsonify({
                "connected": True,
                "message": "Supabase connection successful"
            }), 200
        except Exception as q_err:
            err_str = str(q_err)
            if "42501" in err_str or "permission denied" in err_str.lower():
                return jsonify({
                    "connected": True,
                    "message": "Supabase connected (table access governed by RLS)",
                    "note": "Connection verified"
                }), 200
            else:
                err_clean = re.sub(r'Bearer\s+[A-Za-z0-9_\-\.]+', 'Bearer [REDACTED]', err_str)
                err_clean = re.sub(r'sb_[A-Za-z0-9_-]+', '[REDACTED]', err_clean)
                return jsonify({
                    "connected": False,
                    "error": err_clean,
                    "message": "Supabase query check failed"
                }), 200
    except Exception as e:
        err_msg = str(e)
        err_msg = re.sub(r'sb_[A-Za-z0-9_-]+', '[REDACTED]', err_msg)
        err_msg = re.sub(r'Bearer\s+[A-Za-z0-9_\-\.]+', 'Bearer [REDACTED]', err_msg)
        return jsonify({
            "connected": False,
            "error": err_msg,
            "message": "Supabase connection failed"
        }), 200

@app.route("/api/ai/status", methods=["GET"])
def get_ai_status():
    """
    Returns AI reasoning engine provider, availability, and active model.
    Never exposes API keys or secrets.
    """
    provider_env = os.environ.get("AI_PROVIDER", "").strip().lower()
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    gemini_model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash").strip()
    gemma_model = os.environ.get("GEMMA_MODEL", "gemma3:4b").strip()
    ollama_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")

    if provider_env == "gemini" or (not provider_env and gemini_key):
        return jsonify({
            "provider": "gemini",
            "available": bool(gemini_key),
            "model": gemini_model
        }), 200
    else:
        # Check Ollama connectivity
        ollama_available = False
        try:
            req = urllib.request.Request(f"{ollama_url}/api/tags")
            with urllib.request.urlopen(req, timeout=1.0) as resp:
                ollama_available = (resp.status == 200)
        except Exception:
            ollama_available = False

        return jsonify({
            "provider": "ollama",
            "available": ollama_available,
            "model": gemma_model
        }), 200


@app.route("/api/companies/search", methods=["GET"])
def api_companies_search():
    """
    Standard Global Company Search Endpoint:
    GET /api/companies/search?q=apple
    Returns:
    {
        "query": "apple",
        "results": [ ... ]
    }
    """
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"query": "", "results": []})
    results = search_companies(q)
    return jsonify({
        "query": q,
        "results": results
    })

@app.route("/api/search", methods=["GET"])
def api_search_alias():
    """Autocomplete search endpoint returning array of matches for backwards compatibility."""
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify([])
    return jsonify(search_companies(q))

@app.route("/api/companies", methods=["GET"])
def api_get_companies():
    """
    Returns global company records with optional filtering:
    ?country=Japan&exchange=TSE&q=toyota
    """
    country_filter = request.args.get("country", "").strip()
    exchange_filter = request.args.get("exchange", "").strip()
    q_filter = request.args.get("q", "").strip().lower()

    filtered = []
    for c in GLOBAL_COMPANIES:
        if country_filter and country_filter.lower() != "all" and c["country"].lower() != country_filter.lower():
            continue
        if exchange_filter and exchange_filter.lower() != "all" and c["exchange"].lower() != exchange_filter.lower():
            continue
        if q_filter:
            if q_filter not in c["ticker"].lower() and q_filter not in c["company_name"].lower():
                continue
        filtered.append({
            "ticker": c["ticker"],
            "yahoo_ticker": c.get("yahoo_ticker", c["ticker"]),
            "company_name": c["company_name"],
            "exchange": c["exchange"],
            "country": c["country"],
            "currency": c.get("currency", "USD"),
            "region": c.get("region", "Global")
        })

    return jsonify({
        "total": len(filtered),
        "companies": filtered
    })

@app.route("/api/companies/filters", methods=["GET"])
def api_get_filters():
    """Returns represented countries and exchanges for dynamic UI dropdowns."""
    return jsonify({
        "countries": ["All"] + get_supported_countries(),
        "exchanges": ["All"] + get_supported_exchanges()
    })

@app.route("/api/company/<ticker>", methods=["GET"])
def api_company_info(ticker):
    """Returns company info, latest price, and day change for the company header."""
    info = get_company_info(ticker)
    if not info:
        return jsonify({"error": f"Company '{ticker}' not found."}), 404
    return jsonify(info)

@app.route("/api/markets", methods=["GET"])
def api_markets():
    """
    Returns right-panel global markets watchlist.
    Supports filtering by ?country=... &exchange=... &q=...
    Fulfills Performance Requirement 18:
    Loads metadata instantly without downloading historical data for every company at startup.
    Uses cached/snapshot prices if available.
    """
    country_filter = request.args.get("country", "").strip()
    exchange_filter = request.args.get("exchange", "").strip()
    q_filter = request.args.get("q", "").strip().lower()

    # Base watchlist
    default_watchlist = [
        "AAPL", "MSFT", "NVDA", "TSLA", "AMZN", "GOOGL", "META",
        "TCS.NS", "INFY.NS", "RELIANCE.NS", "SAP.DE", "7203.T",
        "005930.KS", "0700.HK", "ASML.AS", "SHOP.TO", "BHP.AX", "2330.TW"
    ]

    target_items = []
    if not country_filter and not exchange_filter and not q_filter:
        for sym in default_watchlist:
            cat = CATALOG_BY_TICKER.get(sym)
            if cat:
                target_items.append(cat)
    else:
        for c in GLOBAL_COMPANIES:
            if country_filter and country_filter.lower() != "all" and c["country"].lower() != country_filter.lower():
                continue
            if exchange_filter and exchange_filter.lower() != "all" and c["exchange"].lower() != exchange_filter.lower():
                continue
            if q_filter:
                if q_filter not in c["ticker"].lower() and q_filter not in c["company_name"].lower():
                    continue
            target_items.append(c)
            if len(target_items) >= 40:
                break

    now_ts = datetime.now().timestamp()
    markets_data = []
    for cat in target_items:
        sym = cat["ticker"]
        # 1. Check live memory cache
        cached = _MARKET_CACHE.get(sym)
        if cached and (now_ts - cached.get("ts", 0)) < 300:
            markets_data.append(cached["data"])
            continue

        # 2. Check snapshot default prices
        snap = _DEFAULT_WATCHLIST_SNAPSHOT.get(sym)
        latest_p = snap["latest_price"] if snap else None
        prev_c = snap["previous_close"] if snap else None
        chg_pct = snap["daily_change_pct"] if snap else None

        markets_data.append({
            "ticker": sym,
            "company_name": cat["company_name"],
            "exchange": cat["exchange"],
            "country": cat["country"],
            "latest_price": latest_p,
            "previous_close": prev_c,
            "daily_change_pct": chg_pct,
            "latest_available_date": datetime.now().strftime('%Y-%m-%d')
        })

    return jsonify(markets_data)

@app.route("/api/test/<ticker>")
def test_ticker(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")
        if hist.empty:
            return jsonify({"error": f"No data found for ticker '{ticker}' or invalid ticker."}), 404

        num_rows = len(hist)
        latest_close = hist['Close'].iloc[-1]
        return jsonify({
            "ticker": ticker.upper(),
            "data_rows": num_rows,
            "latest_close": float(latest_close)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    ticker_input = data.get("ticker")
    drop_threshold = data.get("drop_threshold")
    window_days = data.get("window_days")
    years = data.get("years")

    # Validation
    if not ticker_input or not isinstance(ticker_input, str) or not ticker_input.strip():
        return jsonify({"error": "Missing or invalid ticker. No matching company found."}), 400

    if drop_threshold is None or not isinstance(drop_threshold, (int, float)) or drop_threshold < 0:
        return jsonify({"error": "Missing, invalid, or negative drop_threshold"}), 400

    if window_days is None or not isinstance(window_days, int) or window_days <= 0:
        return jsonify({"error": "Missing or invalid window_days"}), 400

    if years is None or not isinstance(years, int) or years <= 0:
        return jsonify({"error": "Missing or invalid years"}), 400

    # Resolve company name / alias / ticker to a canonical ticker symbol
    resolved = resolve_company_to_ticker(ticker_input.strip())
    if not resolved["resolved"]:
        return jsonify({"error": f"No matching company found for \"{ticker_input.strip()}\"."}), 404

    ticker = resolved["ticker"]
    print(f"[analyze] Input: {ticker_input!r} -> Resolved ticker: {ticker}", flush=True)

    try:
        results = analyze_stock_drops(
            ticker=ticker,
            drop_threshold=float(drop_threshold),
            window_days=window_days,
            years=years
        )

        company_info = get_company_info(ticker)
        if company_info:
            results["company_info"] = company_info
            results["company_name"] = company_info["company_name"]
            results["exchange"] = company_info["exchange"]
            results["country"] = company_info["country"]
            results["latest_price"] = company_info["latest_price"]
            results["daily_change_pct"] = company_info["daily_change_pct"]

        return jsonify(results)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": f"Analysis error: {str(e)}"}), 500

def call_gemini(sys_prompt: str, user_prompt: str) -> dict:
    """
    Invokes Google Gemini API.
    Uses official google-genai SDK if available, with robust REST API fallback.
    Never logs or leaks API keys.
    """
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        return {
            "success": False,
            "error": "GEMINI_API_KEY is not configured in backend environment."
        }

    model_name = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash").strip()

    # 1. Attempt official google.genai SDK
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=api_key)
        config = types.GenerateContentConfig(
            system_instruction=sys_prompt,
            temperature=0.2,
        )
        response = client.models.generate_content(
            model=model_name,
            contents=user_prompt,
            config=config
        )
        if response and response.text:
            return {
                "success": True,
                "reply": response.text.strip(),
                "model": model_name,
                "provider": "gemini"
            }
    except Exception as sdk_err:
        sdk_err_msg = str(sdk_err)
        sdk_err_msg = re.sub(r'AIza[A-Za-z0-9_-]{30,}', '[REDACTED]', sdk_err_msg)
        print(f"[CHAT] Google GenAI SDK notice ({type(sdk_err).__name__}), attempting REST fallback: {sdk_err_msg}", flush=True)

    # 2. REST API fallback via HTTPS to Generative Language API
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{urllib.parse.quote(model_name)}:generateContent?key={urllib.parse.quote(api_key)}"
        payload = {
            "system_instruction": {
                "parts": [{"text": sys_prompt}]
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": user_prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.2
            }
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    reply_text = "".join(p.get("text", "") for p in parts).strip()
                    return {
                        "success": True,
                        "reply": reply_text,
                        "model": model_name,
                        "provider": "gemini"
                    }
            return {
                "success": False,
                "error": "Gemini API returned an empty response candidate."
            }
    except urllib.error.HTTPError as http_err:
        err_body = http_err.read().decode("utf-8", errors="replace")
        err_body = re.sub(r'AIza[A-Za-z0-9_-]{30,}', '[REDACTED]', err_body)
        err_body = re.sub(r'key=[A-Za-z0-9_-]+', 'key=[REDACTED]', err_body)
        return {
            "success": False,
            "error": f"Gemini API HTTP {http_err.code}: {err_body}"
        }
    except Exception as e:
        err_msg = str(e)
        err_msg = re.sub(r'AIza[A-Za-z0-9_-]{30,}', '[REDACTED]', err_msg)
        return {
            "success": False,
            "error": f"Gemini API request failed: {err_msg}"
        }


def call_ollama(messages: list) -> dict:
    """
    Invokes local Ollama / Gemma 3 for local development.
    """
    model = os.environ.get("GEMMA_MODEL", "gemma3:4b").strip()
    base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
    url = f"{base_url}/api/chat"

    payload = {
        "model": model,
        "messages": messages,
        "stream": False
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return {
                "success": True,
                "reply": data["message"]["content"],
                "model": model,
                "provider": "ollama"
            }
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"success": False, "error": f"Model '{model}' needs to be installed. Run 'ollama run {model}'"}
        return {"success": False, "error": f"Ollama HTTP error: {e.code}"}
    except urllib.error.URLError:
        return {"success": False, "error": "Local AI service (Ollama) is unavailable. Please start Ollama."}
    except Exception as e:
        return {"success": False, "error": f"Local AI error: {str(e)}"}


def ask_ai(sys_prompt: str, user_prompt: str, messages: list) -> dict:
    """
    Dispatches reasoning request to either Gemini (production) or Ollama (local development).
    """
    provider_env = os.environ.get("AI_PROVIDER", "").strip().lower()
    has_gemini_key = bool(os.environ.get("GEMINI_API_KEY", "").strip())

    if provider_env == "gemini" or (not provider_env and has_gemini_key):
        selected_provider = "gemini"
    else:
        selected_provider = "ollama"

    print(f"[CHAT] selected AI provider: {selected_provider}", flush=True)
    print("[CHAT] AI request started", flush=True)

    if selected_provider == "gemini":
        result = call_gemini(sys_prompt, user_prompt)
    else:
        result = call_ollama(messages)

    if result.get("success"):
        print("[CHAT] AI request completed", flush=True)
    else:
        err_msg = result.get("error", "Unknown error")
        print(f"[CHAT] AI provider error: {err_msg}", flush=True)

    return result


@app.route("/api/chat", methods=["POST"])
def chat():
    payload = request.get_json() or {}
    message = payload.get("message", "").strip()
    current_ticker = payload.get("current_ticker", "AAPL").strip().upper()
    drop_threshold = float(payload.get("drop_threshold", 10))
    window_days = int(payload.get("window_days", 5))
    years = int(payload.get("years", 10))
    credits_balance = int(payload.get("credits", 500))

    if not message:
        return jsonify(sanitize_json_value({
            "success": False,
            "error": "Bad request",
            "message": "Message cannot be empty."
        })), 400

    print(f"[CHAT] incoming message: {message}", flush=True)

    msg_lower = message.lower()

    # Identify Intent (Preserve original action_type logic for UI)
    is_compare = "compare" in msg_lower or " vs " in msg_lower or " versus " in msg_lower
    is_explain = "explain" in msg_lower or "why" in msg_lower or "volatility" in msg_lower or "win rate" in msg_lower or "worst" in msg_lower or "mean" in msg_lower
    is_price_query = "latest price" in msg_lower or "current price" in msg_lower or "share price" in msg_lower or "price of" in msg_lower or ("what is" in msg_lower and "price" in msg_lower)

    # 1. Resolve company
    res = resolve_company_to_ticker(message)
    target_ticker = None
    company_name = None

    if res.get("resolved"):
        target_ticker = res["ticker"]
        company_name = res.get("company_name", target_ticker)
        action_type = "analysis"
        credit_cost = 25
    elif res.get("is_conversational"):
        action_type = "conversation"
        credit_cost = 0
    elif is_explain or is_price_query or is_compare:
        # User asks to explain/compare/price without specifying a new company -> use current dashboard ticker
        target_ticker = current_ticker
        company_name = COMPANY_FULL_NAMES.get(target_ticker, target_ticker)
        if is_compare:
            action_type = "comparison"
            credit_cost = 20
        elif is_explain:
            action_type = "explanation"
            credit_cost = 5
        else:
            action_type = "price"
            credit_cost = 5
    else:
        # Unknown company or unresolvable query
        action_type = "unknown_company"
        credit_cost = 0

    print(f"[CHAT] resolved company: {company_name or 'None'}", flush=True)
    print(f"[CHAT] resolved ticker: {target_ticker or 'None'}", flush=True)

    # Check credits before doing heavy work
    if credits_balance < credit_cost and credit_cost > 0:
        return jsonify(sanitize_json_value({
            "success": False,
            "action_type": action_type,
            "credit_cost": credit_cost,
            "credits_deducted": 0,
            "credits_remaining": credits_balance,
            "insufficient_credits": True,
            "reply": f"⚠️ Insufficient AI Credits (Balance: {credits_balance}, Required: {credit_cost})."
        })), 200

    context_str = ""
    analysis_data = None
    card_data = {}
    stakes_info = {}

    def format_num(val):
        if val is None or (isinstance(val, float) and (math.isnan(val) or math.isinf(val))):
            return "N/A"
        return f"{float(val):+.2f}%"

    if target_ticker:
        try:
            analysis_data = analyze_stock_drops(target_ticker, drop_threshold, window_days, years)
            company_info = get_company_info(target_ticker) or {}

            c_name = company_info.get("company_name", company_name or target_ticker)
            c_exch = company_info.get("exchange", "GLOBAL")
            events = analysis_data.get("total_events_found", 0)

            stats = analysis_data.get("summary_statistics", {})
            s30 = stats.get("30_days", {})
            s90 = stats.get("90_days", {})
            s180 = stats.get("180_days", {})

            context_str = f"Company:\n{c_name}\n\nTicker:\n{target_ticker}\n\nExchange:\n{c_exch}\n\n"
            context_str += f"Analysis Parameters:\nDrop threshold: {drop_threshold}%\nWindow: {window_days} trading days\nHistorical period: {years} years\n\n"
            context_str += f"Total Events:\n{events} historical drop events found\n\n"

            def format_stats_block(s, period):
                cnt = s.get('count', 0)
                avg_v = s.get('average_return') if s.get('average_return') is not None else s.get('mean_return')
                med_v = s.get('median_return')
                win_v = s.get('win_rate')
                bst_v = s.get('best_return')
                wst_v = s.get('worst_return')
                win_str = f"{float(win_v):.1f}%" if win_v is not None else "N/A"
                return (
                    f"{period}-day Forward Statistics ({cnt} mature events):\n"
                    f"  Average return: {format_num(avg_v)}\n"
                    f"  Median return: {format_num(med_v)}\n"
                    f"  Win rate: {win_str}\n"
                    f"  Best return: {format_num(bst_v)}\n"
                    f"  Worst return: {format_num(wst_v)}\n\n"
                )

            if events > 0:
                context_str += format_stats_block(s30, 30)
                context_str += format_stats_block(s90, 90)
                context_str += format_stats_block(s180, 180)
            else:
                context_str += "No historical events found matching the specified parameters.\n"

            stakes_info = analysis_data.get("historical_stakes", {})
            stakes = stakes_info.get("stakes", "HIGH")
            emoji = get_stakes_emoji(stakes)

            mean_30 = s30.get("average_return") if s30.get("average_return") is not None else s30.get("mean_return")
            mean_90 = s90.get("average_return") if s90.get("average_return") is not None else s90.get("mean_return")
            mean_180 = s180.get("average_return") if s180.get("average_return") is not None else s180.get("mean_return")

            card_data = {
                "ticker": target_ticker,
                "company_name": c_name,
                "stakes": stakes,
                "stakes_emoji": emoji,
                "events_count": events,
                "avg_30d": f"{mean_30:+.2f}%" if mean_30 is not None else "N/A",
                "avg_90d": f"{mean_90:+.2f}%" if mean_90 is not None else "N/A",
                "avg_180d": f"{mean_180:+.2f}%" if mean_180 is not None else "N/A",
                "avg_30d_num": mean_30,
                "avg_90d_num": mean_90,
                "avg_180d_num": mean_180,
                "why": stakes_info.get("reason", ""),
                "disclaimer": "Historical analysis only. Global companies supported by available Yahoo Finance market coverage."
            }
            analysis_data["company_info"] = company_info
            analysis_data["company_name"] = c_name

            print(f"[CHAT] analysis completed: {events} events", flush=True)
        except Exception as e:
            print(f"Analysis error for {target_ticker}: {e}", flush=True)
            context_str = f"Failed to retrieve data for {target_ticker}: {e}"
            print("[CHAT] analysis completed: error", flush=True)
    elif res.get("is_conversational"):
        context_str = "No specific stock was requested. The user is greeting or having a conversational chat about NoCap Stocks terminal."
        print("[CHAT] analysis completed: conversational", flush=True)
    else:
        extracted_q = res.get("extracted", message)
        context_str = f"The user asked to analyze '{extracted_q}', but this company or ticker could not be resolved in the global catalog (231 companies across 23 countries) or live market feeds. Do NOT invent data for this company."
        print("[CHAT] analysis completed: unresolved company", flush=True)

    sys_prompt = (
        "You are NoCap AI, the historical stock analysis assistant for NoCap Stocks.\n"
        "NoCap Stocks analyzes historical stock-price behavior after significant historical price drops.\n"
        "STRICT RULES:\n"
        "1. Explain historical data ONLY. You are strictly an explanation layer.\n"
        "2. Use ONLY the structured verified facts supplied in the backend context.\n"
        "3. NEVER invent or hallucinate financial data, prices, dates, statistics, returns, events, tickers, or companies.\n"
        "4. If information is missing or not in the context, explicitly state that the backend does not have that information.\n"
        "5. Do NOT predict future prices or provide future forecasts.\n"
        "6. Do NOT provide buy, sell, or hold recommendations or investment advice.\n"
        "7. Do NOT claim that historical performance guarantees future results.\n"
        "8. Clearly distinguish historical facts from interpretation."
    )

    user_prompt = f"Context from backend:\n{context_str}\n\nUser Question:\n{message}"

    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user_prompt}
    ]

    ai_res = ask_ai(sys_prompt, user_prompt, messages)

    if not ai_res.get("success"):
        err_msg = ai_res.get("error", "AI provider unavailable.")
        return jsonify(sanitize_json_value({
            "success": False,
            "error": "AI provider unavailable",
            "message": err_msg,
            "reply": f"NoCap AI error: {err_msg}"
        })), 500

    reply = ai_res.get("reply", "")

    return jsonify(sanitize_json_value({
        "success": True,
        "action_type": action_type,
        "credit_cost": credit_cost,
        "credits_deducted": credit_cost,
        "credits_remaining": max(0, credits_balance - credit_cost),
        "ticker": target_ticker,
        "company_name": card_data.get("company_name", company_name or target_ticker) if card_data else (company_name or target_ticker),
        "card_data": card_data if card_data else None,
        "reply": reply,
        "historical_stakes": stakes_info if stakes_info else None,
        "analysis_data": analysis_data
    })), 200


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1", "yes")
    print(f"Starting NoCap Global Platform server on http://{host}:{port} (debug={debug})")
    app.run(host=host, port=port, debug=debug, use_reloader=False)
