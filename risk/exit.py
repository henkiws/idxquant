def calculate_exit_levels(price, atr):

    stop_loss = price - (atr * 1.5)
    take_profit = price + (atr * 3)

    return {
        "stop_loss": round(stop_loss, 2),
        "take_profit": round(take_profit, 2)
    }
