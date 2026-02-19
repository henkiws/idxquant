import pandas as pd
import ta


def ensure_series(x):
    """
    Convert dataframe column to pandas Series safely
    """
    if isinstance(x, pd.DataFrame):
        return x.iloc[:, 0]

    if isinstance(x, pd.Series):
        return x

    return pd.Series(x.flatten())


def add_indicators(df):

    df = df.copy()

    # ensure all OHLCV are Series
    close = ensure_series(df["Close"])
    high = ensure_series(df["High"])
    low = ensure_series(df["Low"])
    volume = ensure_series(df["Volume"])

    # RSI
    df["rsi"] = ta.momentum.RSIIndicator(close=close).rsi()

    # SMA
    df["sma20"] = ta.trend.SMAIndicator(close=close, window=20).sma_indicator()
    df["sma50"] = ta.trend.SMAIndicator(close=close, window=50).sma_indicator()

    # EMA
    df["ema20"] = ta.trend.EMAIndicator(close=close, window=20).ema_indicator()
    
    # EMA 50
    df["ema50"] = df["Close"].ewm(span=50, adjust=False).mean()

    # MACD
    macd = ta.trend.MACD(close=close)
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()

    # ATR (IMPORTANT for hedge fund risk management)
    df["atr"] = ta.volatility.AverageTrueRange(
        high=high,
        low=low,
        close=close
    ).average_true_range()

    # Volume SMA
    df["volume_sma"] = volume.rolling(20).mean()

    return df
