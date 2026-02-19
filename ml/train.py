import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier


def ensure_series(x):

    if isinstance(x, pd.DataFrame):
        return x.iloc[:, 0]

    if isinstance(x, pd.Series):
        return x

    return pd.Series(x.flatten())


def train(df):

    df = df.copy()

    # FIX Close column
    df["Close"] = ensure_series(df["Close"])

    # create target (5 day forward return)
    df["target"] = (df["Close"].shift(-5) > df["Close"]).astype(int)

    df = df.dropna()

    features = [
        "rsi",
        "macd",
        "macd_signal",
        "sma20",
        "sma50",
        "ema20",
        "ema50",
        "atr",
        "volume_sma"
    ]

    X = df[features]
    y = df["target"]

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=6,
        random_state=42
    )

    model.fit(X, y)

    joblib.dump(model, "model.pkl")

    print("MODEL TRAINED SUCCESSFULLY")
