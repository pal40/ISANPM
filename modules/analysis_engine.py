import pandas as pd
from utils.data_fetcher import fetch_price_data, fetch_fundamentals
from modules.indicators import moving_average, calculate_rsi, support_resistance
from utils.scoring import compute_fundamental_score, compute_technical_signal, final_recommendation

def run_full_analysis(ticker: str) -> dict:
    """
    Wraps the data fetching, indicators, and scoring to provide a complete
    analysis snapshot for the given ticker.
    """
    # 1. Fetch Data
    price_data = fetch_price_data(ticker, period="2y") # longer for 200 DMA
    fundamentals = fetch_fundamentals(ticker)
    
    if price_data is None or price_data.empty:
        return {
            "error": f"Failed to fetch data for {ticker}"
        }

    # Extract current price
    current_price = float(price_data['Close'].iloc[-1])
    
    # 2. Fundamentals
    fund_score = compute_fundamental_score(fundamentals)
    
    # 3. Technicals
    dma_200_series = moving_average(price_data, 200)
    dma_50_series = moving_average(price_data, 50)
    rsi_series = calculate_rsi(price_data, 14)
    support, resistance = support_resistance(price_data, 60) # use ~3 months for S/R

    # Get latest technical values safely 
    dma_200 = float(dma_200_series.iloc[-1]) if dma_200_series is not None and not pd.isna(dma_200_series.iloc[-1]) else None
    dma_50 = float(dma_50_series.iloc[-1]) if dma_50_series is not None and not pd.isna(dma_50_series.iloc[-1]) else None
    rsi = float(rsi_series.iloc[-1]) if rsi_series is not None and not pd.isna(rsi_series.iloc[-1]) else None
    
    # Analyze Signals
    signal_strength, is_above_200 = compute_technical_signal(current_price, rsi, dma_200, support, resistance)
    
    # 4. Final Recommendation
    recommendation = final_recommendation(fund_score, current_price, support, dma_200)
    
    return {
        "ticker": ticker,
        "current_price": current_price,
        "fund_score": fund_score,
        "sentiment": signal_strength,
        "dma_50": dma_50,
        "dma_200": dma_200,
        "rsi": rsi,
        "is_above_200": is_above_200,
        "recommendation": recommendation,
        "support": support,
        "resistance": resistance,
        "price_history": price_data,
        "fundamentals": fundamentals
    }
