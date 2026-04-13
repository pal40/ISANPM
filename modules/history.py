import datetime
import pandas as pd
from database.db import get_session
from database.models import AnalysisHistory

def save_analysis(user_id: int, result: dict):
    """
    Saves an analysis snapshot from run_full_analysis into the database.
    """
    if "error" in result:
        return False
        
    session = get_session()
    try:
        history_entry = AnalysisHistory(
            user_id=user_id,
            ticker=result["ticker"],
            analysis_score=result["fund_score"],
            recommendation=result["recommendation"],
            price=result["current_price"],
            rsi=result["rsi"],
            above_200_dma=result["is_above_200"],
            timestamp=datetime.datetime.utcnow()
        )
        session.add(history_entry)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Failed to save analysis: {e}")
        return False
    finally:
        session.close()

def get_analysis_history(user_id: int, ticker: str) -> list:
    """
    Retrieves all past analytical snapshots for a specific stock for a given user.
    Returns ordered by timestamp descending.
    """
    session = get_session()
    try:
        results = session.query(AnalysisHistory).filter(
            AnalysisHistory.user_id == user_id,
            AnalysisHistory.ticker == ticker
        ).order_by(AnalysisHistory.timestamp.desc()).all()
        
        history = []
        for r in results:
            history.append({
                "id": r.id,
                "ticker": r.ticker,
                "score": r.analysis_score,
                "recommendation": r.recommendation,
                "price": r.price,
                "rsi": r.rsi,
                "above_200_dma": r.above_200_dma,
                "timestamp": r.timestamp
            })
        return history
    finally:
        session.close()

def get_latest_analysis(user_id: int, ticker: str) -> dict:
    """
    Convenience method to get the most recent analysis for display in tables.
    """
    history = get_analysis_history(user_id, ticker)
    if history:
        return history[0]
    return None
