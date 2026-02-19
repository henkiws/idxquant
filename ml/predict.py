import warnings
import joblib
import pandas as pd

from ml.features import FEATURES

_model = None


def load_model():
    global _model
    if _model is None:
        _model = joblib.load("models/model.pkl")
    return _model


def predict_signal(df):
    """
    Returns probability score 0-1 that stock will go up in 5 days.
    """
    model = load_model()

    # ensure we have all features
    missing = [f for f in FEATURES if f not in df.columns]
    if missing:
        raise ValueError(f"Missing features: {missing}")

    # pass DataFrame (not .values) to preserve feature names
    X = df[FEATURES].iloc[-1:]

    # ensure no NaN
    if X.isnull().any().any():
        return 0.5  # neutral if data is bad

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        prob = model.predict_proba(X)[0][1]

    return float(prob)