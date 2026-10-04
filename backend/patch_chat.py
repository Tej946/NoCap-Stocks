import sys

app_path = "app.py"
with open(app_path, "r", encoding="utf-8") as f:
    content = f.read()

# Find the start of chat function
start_str = '@app.route("/api/chat", methods=["POST"])'
end_str = 'if __name__ == "__main__":'

start_idx = content.find(start_str)
end_idx = content.find(end_str)

new_chat = """@app.route("/api/chat", methods=["POST"])
def chat():
    payload = request.get_json() or {}
    message = payload.get("message", "").strip()
    current_ticker = payload.get("current_ticker", "AAPL").strip().upper()
    drop_threshold = float(payload.get("drop_threshold", 10))
    window_days = int(payload.get("window_days", 5))
    years = int(payload.get("years", 10))
    credits_balance = int(payload.get("credits", 500))

    if not message:
        return jsonify({"error": "Message cannot be empty."}), 400

    msg_lower = message.lower()

    # Identify Intent (Preserve original action_type logic for UI)
    is_compare = "compare" in msg_lower or " vs " in msg_lower or " versus " in msg_lower
    is_explain = "explain" in msg_lower or "why" in msg_lower or "volatility" in msg_lower or "win rate" in msg_lower or "worst" in msg_lower or "mean" in msg_lower
    is_price_query = "latest price" in msg_lower or "current price" in msg_lower or "share price" in msg_lower or "price of" in msg_lower or ("what is" in msg_lower and "price" in msg_lower)

    if is_compare:
        action_type = "comparison"
        credit_cost = 20
    elif is_explain:
        action_type = "explanation"
        credit_cost = 5
    elif is_price_query:
        action_type = "price"
        credit_cost = 5
    else:
        action_type = "analysis"
        credit_cost = 25

    # 1. Resolve company
    res = resolve_company_to_ticker(message)
    target_ticker = None
    
    if res["resolved"]:
        target_ticker = res["ticker"]
    else:
        # If unresolved but is explanation/compare/price, try current_ticker if message implies it
        # Actually if they say "Explain the drops", we use current_ticker
        if is_explain or is_price_query or is_compare:
            target_ticker = current_ticker
            
    # Fetch data if we have a target_ticker
    context_str = ""
    analysis_data = None
    card_data = {}
    stakes_info = {}
    
    if target_ticker:
        try:
            analysis_data = analyze_stock_drops(target_ticker, drop_threshold, window_days, years)
            company_info = get_company_info(target_ticker) or {}
            
            c_name = company_info.get("company_name", target_ticker)
            c_exch = company_info.get("exchange", "GLOBAL")
            events = analysis_data.get("total_events_found", 0)
            
            stats = analysis_data.get("summary_statistics", {})
            s30 = stats.get("30_days", {})
            s90 = stats.get("90_days", {})
            s180 = stats.get("180_days", {})
            
            context_str = f"Company:\\n{c_name}\\n\\nTicker:\\n{target_ticker}\\n\\nExchange:\\n{c_exch}\\n\\n"
            context_str += f"Analysis:\\nDrop threshold: {drop_threshold}%\\nWindow: {window_days} days\\nHistorical period: {years} years\\n\\n"
            context_str += f"Events:\\n{events} historical events\\n\\n"
            
            def format_stats(s, period):
                return (
                    f"{period}-day statistics:\\n"
                    f"average: {s.get('average_return', s.get('mean_return', 0)):.2f}%\\n"
                    f"median: {s.get('median_return', 0):.2f}%\\n"
                    f"win rate: {s.get('win_rate', 0):.2f}%\\n"
                    f"best: {s.get('best_return', 0):.2f}%\\n"
                    f"worst: {s.get('worst_return', 0):.2f}%\\n\\n"
                )
            
            if events > 0:
                context_str += format_stats(s30, 30)
                context_str += format_stats(s90, 90)
                context_str += format_stats(s180, 180)
            else:
                context_str += "No historical events found matching these criteria.\\n"
                
            # Prepare card_data and stakes_info for the frontend
            stakes_info = analysis_data.get("historical_stakes", {})
            stakes = stakes_info.get("stakes", "HIGH")
            emoji = get_stakes_emoji(stakes)
            
            mean_30 = s30.get("average_return") if s30.get("average_return") is not None else s30.get("mean_return")
            mean_90 = s90.get("average_return") if s90.get("average_return") is not None else s90.get("mean_return")
            mean_180 = s180.get("average_return") if s180.get("average_return") is not None else s180.get("mean_return")
            
            card_data = {
                "ticker": target_ticker,
                "company_name": c_name,
                "stakes": stakes,
                "stakes_emoji": emoji,
                "events_count": events,
                "avg_30d": f"{mean_30:+.2f}%" if mean_30 is not None else "N/A",
                "avg_90d": f"{mean_90:+.2f}%" if mean_90 is not None else "N/A",
                "avg_180d": f"{mean_180:+.2f}%" if mean_180 is not None else "N/A",
                "avg_30d_num": mean_30,
                "avg_90d_num": mean_90,
                "avg_180d_num": mean_180,
                "why": stakes_info.get("reason", ""),
                "disclaimer": "Historical analysis only. Global companies supported by available Yahoo Finance market coverage."
            }
            analysis_data["company_info"] = company_info
            analysis_data["company_name"] = c_name
        except Exception as e:
            print(f"Analysis error for {target_ticker}: {e}", flush=True)
            context_str = f"Failed to retrieve data for {target_ticker}: {e}"
    else:
        context_str = "No specific company data requested or found."

    # Logging per requirements
    print("CHAT REQUEST", flush=True)
    print(f"USER MESSAGE: {message}", flush=True)
    print(f"RESOLVED COMPANY: {res.get('company_name', 'None') if res['resolved'] else 'None'}", flush=True)
    print(f"RESOLVED TICKER: {target_ticker}", flush=True)
    print(f"DATA SOURCE: {'Backend' if target_ticker else 'None'}", flush=True)

    # Check credits before Gemma
    if credits_balance < credit_cost and action_type != "clarification":
        return jsonify({
            "action_type": action_type,
            "credit_cost": credit_cost,
            "credits_deducted": 0,
            "credits_remaining": credits_balance,
            "insufficient_credits": True,
            "reply": f"⚠️ Insufficient AI Credits (Balance: {credits_balance}, Required: {credit_cost})."
        })

    sys_prompt = (
        "You are NoCap AI, an explanation assistant for NoCap Stocks.\\n"
        "NoCap Stocks analyzes historical stock-price behavior after significant historical price drops.\\n"
        "You explain historical data only.\\n"
        "Use ONLY the structured facts supplied by the backend.\\n"
        "Never invent financial data, prices, dates, statistics, events, or companies.\\n"
        "If information is missing, explicitly say that the backend does not have the information.\\n"
        "Do not predict future prices.\\n"
        "Do not provide buy, sell, or hold recommendations.\\n"
        "Do not claim that historical performance guarantees future results.\\n"
        "Clearly distinguish historical facts from interpretation."
    )
    
    user_prompt = f"Context from backend:\\n{context_str}\\n\\nUser Question:\\n{message}"
    
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user_prompt}
    ]

    gemma_res = ask_gemma(messages)
    
    print(f"GEMMA MODEL: {gemma_res.get('model', 'gemma3:4b')}", flush=True)
    print(f"RESPONSE STATUS: {'Success' if gemma_res['success'] else 'Error'}", flush=True)

    if not gemma_res["success"]:
        return jsonify({
            "error": gemma_res["error"]
        }), 500

    reply = gemma_res["reply"]

    return jsonify({
        "action_type": action_type,
        "credit_cost": credit_cost,
        "credits_deducted": credit_cost,
        "credits_remaining": credits_balance - credit_cost,
        "ticker": target_ticker,
        "company_name": card_data.get("company_name", target_ticker),
        "card_data": card_data,
        "reply": reply,
        "historical_stakes": stakes_info,
        "analysis_data": analysis_data
    })

"""

content = content[:start_idx] + new_chat + content[end_idx:]

with open(app_path, "w", encoding="utf-8") as f:
    f.write(content)
print("SUCCESS")
