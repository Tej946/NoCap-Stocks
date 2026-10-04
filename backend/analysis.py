import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from supabase_cache import get_stock_data

def calculate_historical_stakes(summary_stats: dict, total_events: int) -> dict:
    """
    Computes the Historical Stakes verdict based on historical drop event outcomes:
    - LOW STAKES: lower historical volatility + limited downside
    - MODERATE STAKES: noticeable volatility / mixed outcomes
    - HIGH STAKES: high volatility or larger historical downside
    - INSUFFICIENT DATA: too few historical events
    """
    s180 = summary_stats.get('180_days', {})
    events_180 = s180.get('count', 0)
    vol_180 = s180.get('std_dev')
    worst_180 = s180.get('worst_return')
    win_rate_180 = s180.get('win_rate')

    basis = {
        'events': total_events,
        'volatility_180d': round(float(vol_180), 2) if vol_180 is not None else None,
        'worst_180d': round(float(worst_180), 2) if worst_180 is not None else None,
        'win_rate_180d': round(float(win_rate_180), 2) if win_rate_180 is not None else None
    }

    # Rule 1: INSUFFICIENT DATA
    # Fewer than 3 total events or fewer than 2 mature 180-day events
    if total_events < 3 or events_180 < 2 or vol_180 is None:
        return {
            'stakes': 'INSUFFICIENT DATA',
            'reason': 'Too few historical events to reliably assess pattern outcomes.',
            'basis': basis
        }

    # Rule 2: HIGH STAKES
    # High volatility (>= 25.0) or larger historical downside (worst <= -15.0 or win_rate < 55.0)
    if vol_180 >= 25.0 or (worst_180 is not None and worst_180 <= -15.0) or (win_rate_180 is not None and win_rate_180 < 55.0):
        if vol_180 >= 25.0 and worst_180 is not None and worst_180 <= -15.0:
            reason = "Historical outcomes showed relatively large variation and significant drawdown risk."
        elif vol_180 >= 25.0:
            reason = "Historical outcomes showed relatively large variation across the analyzed events."
        elif worst_180 is not None and worst_180 <= -15.0:
            reason = "Historical outcomes included substantial downside loss scenarios."
        else:
            reason = "Historical win rate across post-drop horizons was relatively low."
        return {
            'stakes': 'HIGH',
            'reason': reason,
            'basis': basis
        }

    # Rule 3: LOW STAKES
    # Lower historical volatility (< 15.0) + limited downside (worst >= -8.0 and win_rate >= 75.0)
    if vol_180 < 15.0 and (worst_180 is not None and worst_180 >= -8.0) and (win_rate_180 is not None and win_rate_180 >= 75.0):
        return {
            'stakes': 'LOW',
            'reason': "Historical outcomes demonstrated lower volatility with limited downside and consistent recovery.",
            'basis': basis
        }

    # Rule 4: MODERATE STAKES
    return {
        'stakes': 'MODERATE',
        'reason': "Historical outcomes showed noticeable volatility and mixed post-drop trajectories.",
        'basis': basis
    }


def analyze_stock_drops(ticker: str, drop_threshold: float, window_days: int, years: int) -> dict:
    """
    Analyzes historical stock data to find events where the stock dropped by at least `drop_threshold`
    percentage within `window_days` trading days, and calculates forward returns for 30, 90, and 180 calendar days.
    """
    now = datetime.now()
    req_start_date = (now - timedelta(days=int(years * 365.25))).strftime('%Y-%m-%d')
    req_end_date = (now + timedelta(days=1)).strftime('%Y-%m-%d')
    req_today_str = now.strftime('%Y-%m-%d')

    # Fetch historical data via Supabase cache with yfinance fallback
    hist, data_source = get_stock_data(ticker=ticker, years=years)

    if hist is None or hist.empty:
        raise ValueError(f"No historical data found for {ticker}")

    # Determine latest available trading date from actual dataset
    raw_max_date = hist.index.max()
    if hasattr(raw_max_date, 'strftime'):
        latest_available_date = raw_max_date.strftime('%Y-%m-%d')
    else:
        latest_available_date = str(raw_max_date)[:10]

    # Debug logging
    print(f"Ticker: {ticker.upper()}", flush=True)
    print(f"Requested start: {req_start_date}", flush=True)
    print(f"Requested end: {req_today_str}", flush=True)
    print(f"Latest available date: {latest_available_date}", flush=True)
    print(f"Data source: {data_source}", flush=True)
    print(f"Rows received: {len(hist)}", flush=True)

    # Ensure index is timezone-naive for easier timedelta math
    if hist.index.tz is not None:
        hist.index = hist.index.tz_localize(None)

    # 1. Calculate the percentage return over the specified rolling window
    hist['Start_Price'] = hist['Close'].shift(window_days)
    hist['Window_Return'] = (hist['Close'] - hist['Start_Price']) / hist['Start_Price'] * 100

    # 2. Find every historical event where the return is less than or equal to the negative drop threshold.
    target_threshold = -abs(drop_threshold)
    drop_events_mask = hist['Window_Return'] <= target_threshold

    events = []
    cooldown_until = -1
    for i in range(len(hist)):
        if drop_events_mask.iloc[i] and i > cooldown_until:
            event_date = hist.index[i]
            start_date = hist.index[i - window_days]
            event_price = hist['Close'].iloc[i]
            start_price = hist['Start_Price'].iloc[i]
            drop_pct = hist['Window_Return'].iloc[i]
            
            events.append({
                'event_date': event_date,
                'start_date': start_date,
                'drop_percentage': drop_pct,
                'start_price': start_price,
                'event_price': event_price,
                'index_pos': i
            })
            
            # Set cooldown
            cooldown_until = i + window_days

    # Forward periods in calendar days
    forward_periods = {
        '30_days': 30,
        '90_days': 90,
        '180_days': 180
    }
    
    results_events = []
    
    for event in events:
        event_date = event['event_date']
        event_price = event['event_price']
        
        event_data = {
            'event_date': event_date.strftime('%Y-%m-%d'),
            'start_date': event['start_date'].strftime('%Y-%m-%d'),
            'drop_percentage': round(event['drop_percentage'], 2),
            'start_price': round(event['start_price'], 2),
            'event_price': round(event_price, 2),
            'forward_returns': {}
        }
        
        for period_name, days in forward_periods.items():
            target_date = event_date + timedelta(days=days)
            future_data = hist.loc[hist.index >= target_date]
            
            if not future_data.empty:
                future_price = future_data['Close'].iloc[0]
                period_return = (future_price - event_price) / event_price * 100
                event_data['forward_returns'][period_name] = round(period_return, 2)
            else:
                event_data['forward_returns'][period_name] = None
                
        results_events.append(event_data)

    # 5. Calculate statistics for each timeframe
    summary_stats = {}
    
    for period_name in forward_periods.keys():
        returns = [e['forward_returns'][period_name] for e in results_events if e['forward_returns'][period_name] is not None]
        
        if returns:
            avg_return = np.mean(returns)
            med_return = np.median(returns)
            std_return = np.std(returns) if len(returns) > 1 else 0.0
            win_rate = (sum(1 for r in returns if r > 0) / len(returns)) * 100
            best_return = max(returns)
            worst_return = min(returns)
            
            summary_stats[period_name] = {
                'count': len(returns),
                'average_return': round(float(avg_return), 2),
                'median_return': round(float(med_return), 2),
                'std_dev': round(float(std_return), 2),
                'win_rate': round(float(win_rate), 2),
                'best_return': round(float(best_return), 2),
                'worst_return': round(float(worst_return), 2)
            }
        else:
            summary_stats[period_name] = {
                'count': 0,
                'average_return': None,
                'median_return': None,
                'std_dev': None,
                'win_rate': None,
                'best_return': None,
                'worst_return': None
            }
            
    # Calculate Historical Stakes verdict
    stakes_verdict = calculate_historical_stakes(summary_stats, len(results_events))

    # 6. Return the results in a clean Python dictionary
    result = {
        'ticker': ticker.upper(),
        'drop_threshold': drop_threshold,
        'window_days': window_days,
        'years': years,
        'data_source': data_source,
        'total_events_found': len(results_events),
        'summary_statistics': summary_stats,
        'historical_stakes': stakes_verdict,
        'stakes': stakes_verdict['stakes'],
        'reason': stakes_verdict['reason'],
        'basis': stakes_verdict['basis'],
        'events': results_events,
        'price_history': [
            {
                'date': d.strftime('%Y-%m-%d') if hasattr(d, 'strftime') else str(d)[:10],
                'open': round(float(o), 2) if pd.notna(o) else round(float(c), 2),
                'high': round(float(h), 2) if pd.notna(h) else round(float(c), 2),
                'low': round(float(l), 2) if pd.notna(l) else round(float(c), 2),
                'close': round(float(c), 2),
                'volume': int(v) if pd.notna(v) else 0
            }
            for d, o, h, l, c, v in zip(
                hist.index,
                hist['Open'] if 'Open' in hist else hist['Close'],
                hist['High'] if 'High' in hist else hist['Close'],
                hist['Low'] if 'Low' in hist else hist['Close'],
                hist['Close'],
                hist['Volume'] if 'Volume' in hist else [0] * len(hist)
            )
        ],
        'data_range': {
            'requested_start': req_start_date,
            'requested_end': req_today_str,
            'latest_available_date': latest_available_date
        },
        'data_metadata': {
            'requested_years': years,
            'requested_start': req_start_date,
            'requested_end': req_today_str,
            'latest_available_date': latest_available_date,
            'actual_data_points': len(hist)
        }
    }
    return result



