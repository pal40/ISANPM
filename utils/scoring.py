def compute_fundamental_score(fundamentals: dict) -> float:
    """
    Computes a fundamental score (0 to 10 points)
    Growth (0-3), Profitability (0-3), Balance Sheet (0-2), Valuation (0-2).
    """
    score = 0.0
    if not fundamentals:
        return 0.0

    # 1. Growth (max 3)
    rev_growth = fundamentals.get("revenue_growth")
    eps_growth = fundamentals.get("eps_growth")
    g_score = 0
    if rev_growth is not None:
        if rev_growth > 0.15: g_score += 1.5
        elif rev_growth > 0.05: g_score += 1.0
        elif rev_growth > 0: g_score += 0.5
    
    if eps_growth is not None:
        if eps_growth > 0.15: g_score += 1.5
        elif eps_growth > 0.05: g_score += 1.0
        elif eps_growth > 0: g_score += 0.5
    
    score += min(3.0, g_score)

    # 2. Profitability (max 3)
    roe = fundamentals.get("roe")
    margin = fundamentals.get("profit_margins")
    p_score = 0
    if roe is not None:
        if roe > 0.20: p_score += 1.5
        elif roe > 0.10: p_score += 1.0
        elif roe > 0: p_score += 0.5
    
    if margin is not None:
        if margin > 0.15: p_score += 1.5
        elif margin > 0.05: p_score += 1.0
        elif margin > 0: p_score += 0.5
        
    score += min(3.0, p_score)

    # 3. Balance Sheet (max 2)
    debt_equity = fundamentals.get("debt_to_equity") # Can be a string/percentage in some systems or absolute
    b_score = 0
    if debt_equity is not None:
        # yfinance often gives absolute e.g. 50 meaning 50%
        # Convert to a sane metric. We assume lower is better.
        if debt_equity < 50: b_score += 2.0
        elif debt_equity < 100: b_score += 1.0
        elif debt_equity < 200: b_score += 0.5
    else:
        # Graceful placeholder score if no data
        b_score += 1.0
        
    score += b_score

    # 4. Valuation (max 2)
    pe = fundamentals.get("pe_ratio")
    v_score = 0
    if pe is not None and pe > 0:
        if pe < 15: v_score += 2.0
        elif pe < 25: v_score += 1.0
        elif pe < 40: v_score += 0.5
    else:
        v_score += 1.0
        
    score += v_score

    return round(score, 1)


def compute_technical_signal(current_price: float, rsi: float, dma_200: float, support: float, resistance: float) -> str:
    """
    Evaluates basic technical signals and creates a qualitative string or returns components.
    Here we'll return a simple sentiment logic string, and boolean if above 200 DMA.
    """
    signals = []
    bullish_points = 0
    
    is_above_200 = False
    
    if rsi is not None:
        if rsi < 30:
            signals.append("RSI Oversold")
            bullish_points += 1
        elif rsi > 70:
            signals.append("RSI Overbought")
            bullish_points -= 1
            
    if dma_200 is not None and current_price is not None:
        if current_price > dma_200:
            is_above_200 = True
            signals.append("Above 200 DMA (Bullish)")
            bullish_points += 1
        else:
            signals.append("Below 200 DMA (Bearish)")
            bullish_points -= 1
            
    if support is not None and current_price is not None:
        # Check if price is within 5% of support
        if current_price <= support * 1.05 and current_price >= support * 0.95:
            signals.append("Near Support")
            bullish_points += 1

    signal_strength = "NEUTRAL"
    if bullish_points >= 2:
        signal_strength = "BULLISH"
    elif bullish_points <= -1:
        signal_strength = "BEARISH"

    return signal_strength, is_above_200


def final_recommendation(fund_score: float, current_price: float, support: float, dma_200: float) -> str:
    """
    Final Recommendation Engine combining fundamental score and basic technical signals.
    """
    if fund_score is None:
        return "HOLD"
        
    # Logic:
    # IF score >= 7 AND price near support -> BUY
    # IF score 5-7 -> HOLD
    # IF score < 5 OR below 200 DMA -> SELL
    
    near_support = False
    is_below_200 = False
    
    if current_price is not None:
        if support is not None and (support * 0.95 <= current_price <= support * 1.05):
            near_support = True
        
        if dma_200 is not None and current_price < dma_200:
            is_below_200 = True

    if fund_score >= 7.0 and near_support:
        return "BUY"
    elif fund_score < 5.0 or is_below_200:
        return "SELL"
    elif fund_score >= 5.0 and fund_score < 7.0:
        return "HOLD"
    elif fund_score >= 7.0 and not near_support:
        # If fund_score is high but not near support, typically HOLD until support level.
        return "HOLD"
        
    return "HOLD"
