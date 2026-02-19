def calculate_exit_levels(price: float, atr: float) -> dict:
    """
    Calculate stop loss and take profit using ATR multiples.
    Stop Loss  = price - (ATR * 2.0)  → 2x ATR below entry
    Take Profit = price + (ATR * 3.0) → 3x ATR above entry (1:1.5 R:R)
    """
    stop_loss   = price - (atr * 2.0)
    take_profit = price + (atr * 3.0)

    # stop loss can't go below zero
    stop_loss = max(stop_loss, price * 0.5)

    return {
        "stop_loss":   round(stop_loss, 2),
        "take_profit": round(take_profit, 2),
        "risk_reward": round((take_profit - price) / (price - stop_loss), 2) if price > stop_loss else 0
    }