import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv("../.env")
url = os.environ.get("SUPABASE_URL")
if url and not url.startswith("http"):
    url = f"https://{url}.supabase.co"
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

supabase = create_client(url, key)

print("--- Querying Supabase for MSFT ---")
res = supabase.table("companies").select("*").ilike("ticker", "%MSFT%").execute()
print("MSFT matches:", res.data)
