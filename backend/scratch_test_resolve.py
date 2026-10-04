import sys
sys.path.append("c:/Users/kaset/OneDrive/Desktop/NoCap-Stocks/backend")
from app import resolve_company_to_ticker, search_companies
print("search_companies NESTLE:", search_companies("NESTLE"))
print("resolve_company_to_ticker NESN.SW:", resolve_company_to_ticker("NESN.SW"))
print("resolve_company_to_ticker NESTLE:", resolve_company_to_ticker("NESTLE"))
print("resolve_company_to_ticker Nestle:", resolve_company_to_ticker("Nestle"))
