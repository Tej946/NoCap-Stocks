import sys
import os
sys.path.append('c:/Users/kaset/OneDrive/Desktop/NoCap-Stocks/backend')
from app import resolve_company_to_ticker

queries = [
    "What is NoCap Stocks?",
    "Explain Puma historical drops",
    "Analyze TCS",
    "What happened after Microsoft had large historical drops?",
    "Analyze somethingxyz123"
]
for q in queries:
    res = resolve_company_to_ticker(q)
    print(f"Q: {q}")
    print(f"Resolved: {res['resolved']}")
    if res['resolved']:
        print(f"Ticker: {res['ticker']}")
    else:
        print(f"Extracted: {res.get('extracted')}")
    print("-" * 20)
