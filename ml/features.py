def create_features(df):

    last = df.iloc[-1]

    return [
        last['MA20'],
        last['MA50'],
        last['RSI']
    ]