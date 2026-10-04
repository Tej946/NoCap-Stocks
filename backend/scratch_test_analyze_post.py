import urllib.request, json
url = "http://127.0.0.1:5000/api/analyze"
data = json.dumps({"ticker": "NESN.SW", "drop_threshold": 10, "window_days": 5, "years": 10}).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode("utf-8")[:200])
except Exception as e:
    print(e.read().decode("utf-8"))
