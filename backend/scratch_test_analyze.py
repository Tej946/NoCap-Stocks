import sys
sys.path.append("c:/Users/kaset/OneDrive/Desktop/NoCap-Stocks/backend")
from app import analyze_stock_drops

try:
    print("Testing NESN.SW:")
    res = analyze_stock_drops("NESN.SW", 10, 5, 10)
    print("Success")
except Exception as e:
    print("Error:", type(e), str(e))
