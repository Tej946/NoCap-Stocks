import urllib.request
import json
import time

facts = """Company: Puma SE
Ticker: PUM.DE
Exchange: XETRA
Country: Germany

Analysis Parameters:
- Drop threshold: 10.0%
- Drop window: 5 trading days
- Historical period: 10 years
- Events found: 16 historical occurrences
- Historical stakes assessment: HIGH (Reason: Significant return dispersion across mature 180-day post-drop holding periods)

30-day Forward Statistics:
- Average return: +3.42%
- Median return: +2.15%
- Win rate: 62.5% (10 of 16 positive)
- Best return: +24.50%
- Worst return: -18.20%

90-day Forward Statistics:
- Average return: +6.80%
- Median return: +5.10%
- Win rate: 68.8% (11 of 16 positive)
- Best return: +38.10%
- Worst return: -22.40%

180-day Forward Statistics:
- Average return: +12.35%
- Median return: +9.40%
- Win rate: 75.0% (12 of 16 positive)
- Best return: +54.20%
- Worst return: -29.80%"""

system_prompt = (
    "You are NoCap AI, an explanation assistant for NoCap Stocks.\n\n"
    "NoCap Stocks analyzes historical stock-price behavior after significant historical price drops.\n\n"
    "You explain historical data only.\n\n"
    "Use ONLY the structured facts supplied by the backend.\n"
    "Never invent financial data, prices, dates, statistics, events, or companies.\n"
    "If information is missing, explicitly say that the backend does not have the information.\n"
    "Do not predict future prices.\n"
    "Do not provide buy, sell, or hold recommendations.\n"
    "Do not claim that historical performance guarantees future results.\n"
    "Clearly distinguish historical facts from interpretation."
)

user_prompt = f"""User Question: Explain Puma historical drops

Structured Facts from Backend:
{facts}

Explain these historical facts clearly and concisely in plain English."""

payload = {
    "model": "gemma3:4b",
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    "stream": False,
    "options": {
        "temperature": 0.2,
        "num_predict": 300
    }
}

req = urllib.request.Request(
    "http://localhost:11434/api/chat",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST"
)

t0 = time.time()
print("Asking Gemma 3 to explain Puma historical drops...")
try:
    with urllib.request.urlopen(req, timeout=90) as r:
        res = json.loads(r.read().decode("utf-8"))
        print(f"Completed in {time.time()-t0:.2f}s:")
        print("------------------------------------------")
        print(res["message"]["content"])
        print("------------------------------------------")
except Exception as e:
    print("Error:", e)
