from data.idx_list import get_idx_stocks
from data.fetch_stock import get_stock
from indicators.technical import add_indicators

from ml.predict import predict_signal
from sentiment.news import get_news
from sentiment.analyzer import score_news

from risk.position import calculate_position_size
from risk.risk_score import calculate_risk_score
from risk.exit import calculate_exit_levels

from notifier.telegram import send

import pandas as pd


PORTFOLIO_SIZE = 100_000_000  # 100 juta rupiah
RISK_PER_TRADE = 0.02
TOP_N = 10

def get_scalar(df, column):

    val = df[column].iloc[-1]

    # if Series -> convert to scalar
    if isinstance(val, pd.Series):
        val = val.iloc[0]

    return float(val)


def run():

    print("\nIDXQuantBot Hedge Fund Scanner running...\n")

    stocks = get_idx_stocks()

    print(f"Scanning {len(stocks)} IDX stocks...\n")

    results = []

    for symbol in stocks:

        try:

            print(f"Analyzing {symbol}")

            df = get_stock(symbol)

            if df is None or df.empty:
                continue

            df = add_indicators(df)

            if df is None or df.empty:
                continue

            # ===== FIX SAFE VALUE EXTRACTION =====

            price = get_scalar(df, "Close")

            if "ATR" in df.columns:
                atr = get_scalar(df, "ATR")
            elif "atr" in df.columns:
                atr = get_scalar(df, "atr")
            else:
                continue

            # skip invalid ATR
            if atr <= 0 or pd.isna(atr):
                continue

            # ===== ML =====

            ml_prob = float(predict_signal(df))

            # ===== SENTIMENT =====

            news = get_news(symbol)
            sentiment = float(score_news(news))

            # ===== RISK =====

            risk_score = float(calculate_risk_score(price, atr))

            exit_levels = calculate_exit_levels(price, atr)

            stop_loss = float(exit_levels["stop_loss"])
            take_profit = float(exit_levels["take_profit"])

            # ===== FINAL SCORE =====

            score = (
                ml_prob * 0.5 +
                sentiment * 0.2 +
                risk_score * 0.3
            )

            # ===== POSITION SIZE =====

            shares = calculate_position_size(
                PORTFOLIO_SIZE,
                RISK_PER_TRADE,
                price,
                stop_loss
            )

            # ===== SIGNAL =====

            if score > 0.65:
                signal = "BUY"
            elif score < 0.45:
                signal = "SELL"
            else:
                signal = "HOLD"

            results.append({

                "symbol": symbol,
                "price": price,
                "score": score,
                "signal": signal,
                "ml_prob": ml_prob,
                "sentiment": sentiment,
                "risk_score": risk_score,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "shares": shares

            })

        except Exception as e:

            print(f"Error {symbol}: {e}")


    if len(results) == 0:

        print("No signals found.")
        return


    # sort best first
    results = sorted(results, key=lambda x: x["score"], reverse=True)


    # ===== BUILD MESSAGE =====

    message = "📊 IDXQuantBot Hedge Fund Signals\n\n"

    for r in results[:TOP_N]:

        msg = (
            f"{r['symbol']}\n"
            f"Signal: {r['signal']}\n"
            f"Price: {r['price']:.0f}\n"
            f"Score: {r['score']:.2f}\n"
            f"Stop Loss: {r['stop_loss']:.0f}\n"
            f"Take Profit: {r['take_profit']:.0f}\n"
            f"Shares: {r['shares']}\n\n"
        )

        print(msg)

        message += msg


    send(message)

    print("\nTelegram notification sent.")
    print("Done.")


if __name__ == "__main__":

    run()
