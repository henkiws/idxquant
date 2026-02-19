def calculate_risk_score(price: float, atr: float) -> float:
    """
    Calculate normalized risk score (0 to 1) based on ATR volatility ratio.
    Higher score = lower risk = better for trading.
    """
    if atr <= 0 or price <= 0:
        return 0.0

    volatility_ratio = atr / price

    # Score inversely proportional to volatility
    if volatility_ratio < 0.01:
        return 1.0
    elif volatility_ratio < 0.02:
        return 0.9
    elif volatility_ratio < 0.03:
        return 0.75
    elif volatility_ratio < 0.04:
        return 0.60
    elif volatility_ratio < 0.06:
        return 0.45
    elif volatility_ratio < 0.08:
        return 0.30
    else:
        return 0.15