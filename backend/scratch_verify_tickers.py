import sys
sys.path.append("c:/Users/kaset/OneDrive/Desktop/NoCap-Stocks/backend")
from supabase_client import get_supabase_client

tickers = ["AAPL", "MSFT", "NVDA", "PUM.DE", "TCS.NS", "INFY.NS", "SAP.DE", "7203.T", "005930.KS", "0700.HK", "SHOP.TO", "BHP.AX", "ASML.AS", "NESN.SW"]

client = get_supabase_client()
res = client.table("companies").select("ticker").in_("ticker", tickers).execute()
found = {r["ticker"] for r in res.data}

for t in tickers:
    print(f"{t}: {'Found' if t in found else 'Missing'}")
