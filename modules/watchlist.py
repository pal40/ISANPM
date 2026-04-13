from database.db import get_session
from database.models import Watchlist

def add_to_watchlist(user_id: int, ticker: str, display_name: str) -> bool:
    """
    Adds a stock to the user's watchlist.
    Returns True if added successfully, False if already exists.
    """
    session = get_session()
    try:
        # Check if already exists
        exists = session.query(Watchlist).filter(
            Watchlist.user_id == user_id, 
            Watchlist.ticker == ticker
        ).first()
        
        if exists:
            return False
            
        new_entry = Watchlist(user_id=user_id, ticker=ticker, display_name=display_name)
        session.add(new_entry)
        session.commit()
        return True
    finally:
        session.close()

def remove_from_watchlist(item_id: int):
    """
    Removes an item from the watchlist by its primary key ID.
    """
    session = get_session()
    try:
        item = session.query(Watchlist).filter(Watchlist.id == item_id).first()
        if item:
            session.delete(item)
            session.commit()
    finally:
        session.close()

def get_watchlist(user_id: int) -> list:
    """
    Retrieves the complete watchlist for a specific user.
    """
    session = get_session()
    try:
        results = session.query(Watchlist).filter(Watchlist.user_id == user_id).all()
        # Convert to dictionary or list of objects
        watchlist = []
        for r in results:
            watchlist.append({
                "id": r.id,
                "ticker": r.ticker,
                "display_name": r.display_name
            })
        return watchlist
    finally:
        session.close()
