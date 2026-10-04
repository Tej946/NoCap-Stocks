import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv("../.env")
url = os.environ.get("SUPABASE_URL")
if url and not url.startswith("http"):
    url = f"https://{url}.supabase.co"
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

supabase = create_client(url, key)

print("--- Querying Supabase for Nestle/NESN.SW ---")
res = supabase.table("companies").select("*").ilike("ticker", "%NESN%").execute()
print("NESN matches:", res.data)

res2 = supabase.table("companies").select("*").ilike("company_name", "%Nestl%").execute()
print("Nestle matches:", res2.data)

res_count = supabase.table("companies").select("*", count="exact").execute()
print("Total companies:", res_count.count)
