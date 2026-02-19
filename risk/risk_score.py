def calculate_risk_score(price, atr):

    if atr <= 0:
        return 0

    risk_percent = atr / price

    if risk_percent < 0.02:
        return 90
    elif risk_percent < 0.04:
        return 70
    elif risk_percent < 0.06:
        return 50
    else:
        return 30
