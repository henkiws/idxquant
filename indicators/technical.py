import pandas as pd
import ta


def ensure_series(x) -> pd.Series:
    """Safely convert any column to a flat pandas Series of floats."""
    if isinstance(x, pd.DataFrame):
        x = x.iloc[:, 0]
    if not isinstance(x, pd.Series):
        x = pd.Series(x.flatten())
    return x.astype(float)


def add_indicators(df: pd.DataFrame) -> pd.DataFrame | None:
    """
    Add all technical indicators to dataframe.
    Returns None if dataframe is too short or broken.
    """
    if df is None or df.empty or len(df) < 60:
        return None

    df = df.copy()

    # flatten MultiIndex just in case
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # remove duplicate columns
    df = df.loc[:, ~df.columns.duplicated(keep="first")]

    try:
        close  = ensure_series(df["Close"])
        high   = ensure_series(df["High"])
        low    = ensure_series(df["Low"])
        volume = ensure_series(df["Volume"])

        # RSI
        df["rsi"] = ta.momentum.RSIIndicator(close=close, window=14).rsi()

        # SMA
        df["sma20"] = ta.trend.SMAIndicator(close=close, window=20).sma_indicator()
        df["sma50"] = ta.trend.SMAIndicator(close=close, window=50).sma_indicator()

        # EMA
        df["ema20"] = ta.trend.EMAIndicator(close=close, window=20).ema_indicator()
        df["ema50"] = ta.trend.EMAIndicator(close=close, window=50).ema_indicator()

        # MACD
        macd_obj = ta.trend.MACD(close=close)
        df["macd"]        = macd_obj.macd()
        df["macd_signal"] = macd_obj.macd_signal()

        # ATR
        df["atr"] = ta.volatility.AverageTrueRange(
            high=high, low=low, close=close, window=14
        ).average_true_range()

        # Volume SMA
        df["volume_sma"] = volume.rolling(window=20).mean()

        # drop rows where any indicator is NaN
        indicator_cols = [
            "rsi", "sma20", "sma50", "ema20", "ema50",
            "macd", "macd_signal", "atr", "volume_sma"
        ]
        df = df.dropna(subset=indicator_cols)

        if df.empty:
            return None

        df = df.reset_index(drop=True)

        return df

    except Exception as e:
        print(f"[add_indicators] Error: {e}")
        return None