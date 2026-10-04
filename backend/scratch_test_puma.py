import sys
sys.path.append("c:/Users/kaset/OneDrive/Desktop/NoCap-Stocks/backend")
from app import resolve_company_to_ticker

print("puma:", resolve_company_to_ticker("puma"))
print("Puma:", resolve_company_to_ticker("Puma"))
print("PUMA SE:", resolve_company_to_ticker("PUMA SE"))
