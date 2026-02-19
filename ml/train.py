import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from ml.features import FEATURES


def ensure_series(x):
    if isinstance(x, pd.DataFrame):
        return x.iloc[:, 0]
    if isinstance(x, pd.Series):
        return x
    return pd.Series(x.flatten())


def train(df):

    df = df.copy()

    # flatten multi-index columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # remove duplicate columns
    df = df.loc[:, ~df.columns.duplicated(keep="first")]

    # force Close to Series
    df["Close"] = ensure_series(df["Close"]).astype(float)

    # target: did price go up 5 days later?
    df["target"] = (df["Close"].shift(-5) > df["Close"]).astype(int)

    # drop rows missing features or target
    df = df.dropna(subset=FEATURES + ["target"])

    if len(df) < 100:
        print(f"Not enough data to train: {len(df)} rows")
        return

    X = df[FEATURES]
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=False
    )

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=8,
        min_samples_leaf=10,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\nModel Evaluation:")
    print(classification_report(y_test, y_pred))

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/model.pkl")

    print("MODEL SAVED TO models/model.pkl")