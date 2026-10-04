import urllib.request, urllib.parse, json

queries = [
    "Nestle", "Nestlé", "NESN", "NESN.SW",
    "Microsoft", "TCS", "Puma",
    "somethingxyz123"
]

for q in queries:
    url = f"http://127.0.0.1:5000/api/companies/search?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            results = data.get("results", [])
            first = results[0]["ticker"] if results else "NO MATCH"
            print(f"{q} -> {first}")
    except Exception as e:
        print(f"{q} -> ERROR: {e}")
