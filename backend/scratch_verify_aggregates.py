import sys
sys.path.append("c:/Users/kaset/OneDrive/Desktop/NoCap-Stocks/backend")
from supabase_client import get_supabase_client

client = get_supabase_client()
res = client.table("companies").select("country, exchange").execute()

countries = set(r["country"] for r in res.data if r.get("country"))
exchanges = set(r["exchange"] for r in res.data if r.get("exchange"))

print(f"Total Companies: {len(res.data)}")
print(f"Total Countries: {len(countries)}")
print(f"Total Exchanges: {len(exchanges)}")
