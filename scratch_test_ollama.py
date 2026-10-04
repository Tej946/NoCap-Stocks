import urllib.request
import json
import time

url = "http://localhost:11434/api/chat"
payload = {
    "model": "gemma3:4b",
    "messages": [
        {"role": "user", "content": "Say hello in 5 words."}
    ],
    "stream": False,
    "options": {
        "num_predict": 50,
        "temperature": 0.2
    }
}

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")

print("Sending request to Ollama...")
t0 = time.time()
try:
    with urllib.request.urlopen(req, timeout=120) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        elapsed = time.time() - t0
        print(f"Response in {elapsed:.2f}s:")
        print(res.get("message", {}).get("content"))
except Exception as e:
    print(f"Error after {time.time()-t0:.2f}s: {e}")
