import urllib.request, urllib.parse, json
q = "puma"
url = f"http://127.0.0.1:5000/api/companies/search?q={urllib.parse.quote(q)}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("puma search:", data.get("results", []))
except Exception as e:
    print(e)
