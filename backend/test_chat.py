import sys
import os
import json
import logging

logging.basicConfig(level=logging.INFO)

sys.path.append('c:/Users/kaset/OneDrive/Desktop/NoCap-Stocks/backend')
from app import app

client = app.test_client()

queries = [
    "What is NoCap Stocks?",
    "Explain Puma historical drops",
    "Analyze TCS",
    "What happened after Microsoft had large historical drops?",
    "Analyze somethingxyz123"
]

for q in queries:
    print(f"\\n--- Testing: {q} ---")
    response = client.post('/api/chat', json={"message": q})
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.get_json()
        print(f"Action Type: {data.get('action_type')}")
        print(f"Ticker: {data.get('ticker')}")
        print(f"Reply:\\n{data.get('reply')[:150]}...")
    else:
        print(f"Error:\\n{response.get_data(as_text=True)}")
