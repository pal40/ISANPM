# A curated list of top Indian stocks for intelligent search
INDIAN_STOCKS = [
    {"name": "Reliance Industries", "ticker": "RELIANCE.NS"},
    {"name": "Tata Consultancy Services", "ticker": "TCS.NS"},
    {"name": "HDFC Bank", "ticker": "HDFCBANK.NS"},
    {"name": "ICICI Bank", "ticker": "ICICIBANK.NS"},
    {"name": "Infosys", "ticker": "INFY.NS"},
    {"name": "State Bank of India", "ticker": "SBIN.NS"},
    {"name": "Bharti Airtel", "ticker": "BHARTIARTL.NS"},
    {"name": "Hindustan Unilever", "ticker": "HINDUNILVR.NS"},
    {"name": "ITC", "ticker": "ITC.NS"},
    {"name": "Larsen & Toubro", "ticker": "LT.NS"},
    {"name": "HCL Technologies", "ticker": "HCLTECH.NS"},
    {"name": "Axis Bank", "ticker": "AXISBANK.NS"},
    {"name": "Bajaj Finance", "ticker": "BAJFINANCE.NS"},
    {"name": "Kotak Mahindra Bank", "ticker": "KOTAKBANK.NS"},
    {"name": "Sun Pharmaceutical", "ticker": "SUNPHARMA.NS"},
    {"name": "Tata Motors", "ticker": "TATAMOTORS.NS"},
    {"name": "Maruti Suzuki", "ticker": "MARUTI.NS"},
    {"name": "Asian Paints", "ticker": "ASIANPAINT.NS"},
    {"name": "Wipro", "ticker": "WIPRO.NS"},
    {"name": "UltraTech Cement", "ticker": "ULTRACEMCO.NS"},
    {"name": "Mahindra & Mahindra", "ticker": "M&M.NS"},
    {"name": "Nestle India", "ticker": "NESTLEIND.NS"},
    {"name": "Titan Company", "ticker": "TITAN.NS"},
    {"name": "Power Grid Corporation", "ticker": "POWERGRID.NS"},
    {"name": "Adani Enterprises", "ticker": "ADANIENT.NS"},
    {"name": "Adani Ports", "ticker": "ADANIPORTS.NS"},
    {"name": "Bajaj Finserv", "ticker": "BAJAJFINSV.NS"},
    {"name": "Tata Steel", "ticker": "TATASTEEL.NS"},
    {"name": "NTPC", "ticker": "NTPC.NS"},
    {"name": "IndusInd Bank", "ticker": "INDUSINDBK.NS"},
    {"name": "Hindalco Industries", "ticker": "HINDALCO.NS"},
    {"name": "Tech Mahindra", "ticker": "TECHM.NS"},
    {"name": "Grasim Industries", "ticker": "GRASIM.NS"},
    {"name": "JSW Steel", "ticker": "JSWSTEEL.NS"},
    {"name": "Cipla", "ticker": "CIPLA.NS"},
    {"name": "Dr. Reddy's Laboratories", "ticker": "DRREDDY.NS"},
    {"name": "Bharat Petroleum", "ticker": "BPCL.NS"},
    {"name": "SBI Life Insurance", "ticker": "SBILIFE.NS"},
    {"name": "HDFC Life Insurance", "ticker": "HDFCLIFE.NS"},
    {"name": "Eicher Motors", "ticker": "EICHERMOT.NS"},
    {"name": "Divi's Laboratories", "ticker": "DIVISLAB.NS"},
    {"name": "Britannia Industries", "ticker": "BRITANNIA.NS"},
    {"name": "Apollo Hospitals", "ticker": "APOLLOHOSP.NS"},
    {"name": "Coal India", "ticker": "COALINDIA.NS"},
    {"name": "Tata Consumer Products", "ticker": "TATACONSUM.NS"},
    {"name": "Hero MotoCorp", "ticker": "HEROMOTOCO.NS"},
    {"name": "UPL", "ticker": "UPL.NS"},
    {"name": "ONGC", "ticker": "ONGC.NS"},
]

def search_stock(query: str, stock_list: list = None) -> list:
    """
    Given a search query, returns a list of dictionaries that match the query
    in their display name.
    """
    if stock_list is None:
        stock_list = INDIAN_STOCKS
        
    query = query.lower().strip()
    if not query:
        return []
        
    results = [s for s in stock_list if query in s['name'].lower() or query in s['ticker'].lower()]
    return results[:10]
