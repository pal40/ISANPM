import yfinance as yf
import pandas as pd

def fetch_price_data(ticker: str, period: str = "1y") -> pd.DataFrame:
    """
    Fetches historical price data using yfinance.
    period can be '1y', 'ytd', 'max', '2y', etc.
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        if df.empty:
            return None
        return df
    except Exception as e:
        print(f"Error fetching price data for {ticker}: {e}")
        return None

def fetch_fundamentals(ticker: str) -> dict:
    """
    Fetches fundamental data for the given ticker.
    """
    try:
        stock = yf.Ticker(ticker)
        # Using info dictionary which is cached and faster
        info = stock.info
        
        # Extract basic metrics and handle missing gracefully
        fundamentals = {
            "pe_ratio": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "roe": info.get("returnOnEquity"),
            "debt_to_equity": info.get("debtToEquity"),
            "revenue_growth": info.get("revenueGrowth"),
            "eps_growth": info.get("earningsGrowth"),
            "profit_margins": info.get("profitMargins"),
            "price_to_book": info.get("priceToBook"),
            "current_price": info.get("currentPrice", info.get("regularMarketPrice")),
        }
        return fundamentals
    except Exception as e:
        print(f"Error fetching fundamentals for {ticker}: {e}")
        return None

def fetch_current_price(ticker: str) -> float:
    """
    Fetches only the current price for a lightweight call
    """
    try:
        stock = yf.Ticker(ticker)
        # fast info alternative if available
        # fallback to history day 1 if needed
        data = stock.history(period="1d")
        if not data.empty:
            return float(data['Close'].iloc[-1])
        return None
    except Exception:
        return None
