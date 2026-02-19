import pandas as pd
import yfinance as yf


def get_stock(symbol: str, period: str = "2y") -> pd.DataFrame | None:
    """
    Download OHLCV data for an IDX stock.
    Returns clean single-index DataFrame or None on failure.
    """
    try:
        df = yf.download(
            symbol,
            period=period,
            interval="1d",
            progress=False,
            auto_adjust=True
        )

        if df is None or df.empty:
            return None

        # flatten MultiIndex columns (yfinance sometimes returns these)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # remove duplicate columns
        df = df.loc[:, ~df.columns.duplicated(keep="first")]

        # ensure standard columns exist
        required = ["Open", "High", "Low", "Close", "Volume"]
        for col in required:
            if col not in df.columns:
                return None

        # force all OHLCV to float Series
        for col in required:
            val = df[col]
            if isinstance(val, pd.DataFrame):
                df[col] = val.iloc[:, 0].astype(float)
            else:
                df[col] = val.astype(float)

        df = df.dropna(subset=["Close"])
        df = df[df["Close"] > 0]

        if len(df) < 60:
            return None

        df = df.reset_index(drop=False)  # keep Date as column

        return df

    except Exception as e:
        print(f"[fetch_stock] Error {symbol}: {e}")
        return None