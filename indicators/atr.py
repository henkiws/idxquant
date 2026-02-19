def calculate_atr(df, period=14):

    high_low = df["High"] - df["Low"]

    high_close = abs(df["High"] - df["Close"].shift())
    low_close = abs(df["Low"] - df["Close"].shift())

    tr = high_low.combine(high_close, max).combine(low_close, max)

    atr = tr.rolling(period).mean()

    return atr.iloc[-1]
