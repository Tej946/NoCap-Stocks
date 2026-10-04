import sys
sys.path.append("c:/Users/kaset/OneDrive/Desktop/NoCap-Stocks/backend")
from supabase_client import get_supabase_client

try:
    client = get_supabase_client()
    print("URL used:", client.supabase_url)
    res = client.table("companies").select("*", count="exact").limit(1).execute()
    print("Exact count:", res.count)
except Exception as e:
    print("Error:", e)
