import pandas as pd
import numpy as np

def moving_average(data: pd.DataFrame, window: int, column: str = "Close") -> pd.Series:
    """
    Calculates Simple Moving Average
    """
    if data is None or data.empty or len(data) < window:
        return None
    return data[column].rolling(window=window).mean()

def calculate_rsi(data: pd.DataFrame, window: int = 14, column: str = "Close") -> pd.Series:
    """
    Calculates Relative Strength Index (RSI).
    """
    if data is None or data.empty or len(data) <= window:
        return None
        
    delta = data[column].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)

    # Calculate exponential moving average 
    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()
    
    # Calculate RS
    rs = avg_gain / avg_loss
    
    # Calculate RSI
    rsi = 100 - (100 / (1 + rs))
    return rsi

def support_resistance(data: pd.DataFrame, window: int = 20) -> tuple:
    """
    Calculates a simple recent support (min low) and resistance (max high)
    """
    if data is None or data.empty or len(data) < window:
        return None, None
        
    recent_data = data.tail(window)
    support = recent_data['Low'].min()
    resistance = recent_data['High'].max()
    return support, resistance
