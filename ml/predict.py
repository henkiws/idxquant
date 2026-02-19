import joblib


model = joblib.load("models/model.pkl")


def predict_signal(df):

    features = ["rsi","macd","macd_signal","ema20","ema50"]

    X = df[features].iloc[-1:].values

    prob = model.predict_proba(X)[0][1]

    return prob
