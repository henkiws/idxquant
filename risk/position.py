def calculate_position_size(

    portfolio_size,
    risk_per_trade,
    entry_price,
    stop_loss

):

    risk_amount = portfolio_size * risk_per_trade

    risk_per_share = entry_price - stop_loss

    if risk_per_share <= 0:
        return 0

    shares = int(risk_amount / risk_per_share)

    return shares
