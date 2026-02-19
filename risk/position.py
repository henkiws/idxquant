def calculate_position_size(
    portfolio_size: float,
    risk_per_trade: float,
    entry_price: float,
    stop_loss: float
) -> int:
    """
    Calculate number of shares to buy based on fixed risk per trade.

    Formula:
        risk_amount = portfolio_size * risk_per_trade
        shares = risk_amount / (entry_price - stop_loss)
    """
    if entry_price <= 0 or stop_loss <= 0:
        return 0

    risk_per_share = entry_price - stop_loss

    if risk_per_share <= 0:
        return 0

    risk_amount = portfolio_size * risk_per_trade
    shares = int(risk_amount / risk_per_share)

    # cap at max 20% of portfolio in single position
    max_shares = int((portfolio_size * 0.20) / entry_price)
    shares = min(shares, max_shares)

    return max(shares, 0)