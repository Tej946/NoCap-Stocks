import urllib.request, json

def test_analyze(ticker_input, expected_ticker=None):
    url = "http://127.0.0.1:5000/api/analyze"
    payload = json.dumps({
        "ticker": ticker_input,
        "drop_threshold": 10.0,
        "window_days": 5,
        "years": 1
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            got = data.get("ticker") or data.get("company_info", {}).get("ticker") or "?"
            match = "✓" if (expected_ticker is None or got == expected_ticker) else "✗"
            print(f"[{match}] analyze('{ticker_input}') -> ticker={got}  company={data.get('company_name','?')}")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"[✗] analyze('{ticker_input}') -> HTTP {e.code}: {body}")
    except Exception as e:
        print(f"[✗] analyze('{ticker_input}') -> ERROR: {e}")

def test_search(q, expected_first=None):
    url = f"http://127.0.0.1:5000/api/companies/search?q={urllib.request.quote(q)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            results = data.get("results", [])
            first = results[0]["ticker"] if results else "NO MATCH"
            match = "✓" if (expected_first is None or first == expected_first) else "✗"
            print(f"[{match}] search('{q}') -> {first}")
    except Exception as e:
        print(f"[✗] search('{q}') -> ERROR: {e}")

print("=== /api/analyze resolution tests ===")
test_analyze("Puma",          "PUM.DE")
test_analyze("puma",          "PUM.DE")
test_analyze("PUMA",          "PUM.DE")
test_analyze("PUM.DE",        "PUM.DE")
test_analyze("PUM",           "PUM.DE")
test_analyze("PUMA SE",       "PUM.DE")
test_analyze("Nestle",        "NESN.SW")
test_analyze("Microsoft",     "MSFT")
test_analyze("TCS",           "TCS.NS")
test_analyze("somethingxyz123", None)

print("\n=== /api/companies/search tests ===")
test_search("Puma",          "PUM.DE")
test_search("puma",          "PUM.DE")
test_search("PUM.DE",        "PUM.DE")
test_search("PUM",           "PUM.DE")
test_search("PUMA SE",       "PUM.DE")
test_search("Nestle",        "NESN.SW")
test_search("Microsoft",     "MSFT")
test_search("TCS",           "TCS.NS")
test_search("somethingxyz123", "NO MATCH")
