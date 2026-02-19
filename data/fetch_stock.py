import yfinance as yf


def get_stock(symbol):

    try:

        df = yf.download(
            symbol,
            period="2y",
            interval="1d",
            progress=False
        )

        if df is None or len(df) == 0:
            return None

        df = df.dropna()

        return df

    except Exception as e:

        print(f"Download error: {e}")

        return None
