def calculate_stop_loss(price, atr):

    return round(price - atr*2,2)
