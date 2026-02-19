import pandas as pd

from data.idx_list import get_idx_stocks
from data.fetch_stock import get_stock
from indicators.technical import add_indicators
from ml.predict import predict_signal
from sentiment.news import get_news
from sentiment.analyzer import score_news, normalize_sentiment
from risk.position import calculate_position_size
from risk.risk_score import calculate_risk_score
from risk.exit import calculate_exit_levels
from notifier.telegram import send


# ── Portfolio Settings ────────────────────────────────────────────────────────
PORTFOLIO_SIZE  = 100_000_000   # 100 juta rupiah
RISK_PER_TRADE  = 0.02          # 2% risk per trade
TOP_N           = 10            # top stocks to report

# ── Score Weights ─────────────────────────────────────────────────────────────
W_ML        = 0.50
W_SENTIMENT = 0.20
W_RISK      = 0.30


def safe_scalar(df: pd.DataFrame, column: str) -> float:
    """Safely extract last value from a column as float."""
    val = df[column].iloc[-1]
    if isinstance(val, pd.Series):
        val = val.iloc[0]
    return float(val)


def get_signal(score: float) -> str:
    if score > 0.65:
        return "🟢 BUY"
    elif score < 0.45:
        return "🔴 SELL"
    else:
        return "🟡 HOLD"


def run():
    print("\n" + "="*60)
    print("  IDXQuantBot — Hedge Fund Scanner")
    print("="*60 + "\n")

    stocks = get_idx_stocks()
    print(f"Scanning {len(stocks)} IDX stocks...\n")

    results = []

    for symbol in stocks:
        try:
            print(f"  Analyzing {symbol}...", end=" ")

            # ── Fetch & validate data ─────────────────────────────────────
            df = get_stock(symbol)
            if df is None or df.empty:
                print("SKIP (no data)")
                continue

            # ── Add indicators ────────────────────────────────────────────
            df = add_indicators(df)
            if df is None or df.empty:
                print("SKIP (indicators failed)")
                continue

            # ── Extract price & ATR ───────────────────────────────────────
            price = safe_scalar(df, "Close")
            atr   = safe_scalar(df, "atr")

            if price <= 0 or atr <= 0 or pd.isna(price) or pd.isna(atr):
                print("SKIP (invalid price/ATR)")
                continue

            # ── ML prediction ─────────────────────────────────────────────
            ml_prob = predict_signal(df)

            # ── Sentiment ─────────────────────────────────────────────────
            headlines   = get_news(symbol)
            raw_sent    = score_news(headlines)
            sentiment   = normalize_sentiment(raw_sent)   # convert to 0–1

            # ── Risk ──────────────────────────────────────────────────────
            risk_score  = calculate_risk_score(price, atr)
            exit_levels = calculate_exit_levels(price, atr)
            stop_loss   = exit_levels["stop_loss"]
            take_profit = exit_levels["take_profit"]
            risk_reward = exit_levels["risk_reward"]

            # ── Final composite score ─────────────────────────────────────
            score = (
                ml_prob   * W_ML +
                sentiment * W_SENTIMENT +
                risk_score * W_RISK
            )

            # ── Position sizing ───────────────────────────────────────────
            shares = calculate_position_size(
                PORTFOLIO_SIZE, RISK_PER_TRADE, price, stop_loss
            )

            capital_used = shares * price

            results.append({
                "symbol":       symbol,
                "price":        price,
                "score":        score,
                "signal":       get_signal(score),
                "ml_prob":      ml_prob,
                "sentiment":    sentiment,
                "raw_sent":     raw_sent,
                "risk_score":   risk_score,
                "stop_loss":    stop_loss,
                "take_profit":  take_profit,
                "risk_reward":  risk_reward,
                "shares":       shares,
                "capital_used": capital_used,
            })

            print(f"OK  score={score:.3f}  signal={get_signal(score)}")

        except Exception as e:
            print(f"ERROR ({e})")

    # ── Rank & report ─────────────────────────────────────────────────────────
    if not results:
        print("\nNo valid signals found.")
        send("IDXQuantBot: No valid signals found today.")
        return

    results.sort(key=lambda x: x["score"], reverse=True)

    print(f"\n{'='*60}")
    print(f"  TOP {TOP_N} SIGNALS")
    print(f"{'='*60}\n")

    message = "📊 <b>IDXQuantBot — Hedge Fund Signals</b>\n\n"
    message += f"Portfolio: Rp {PORTFOLIO_SIZE:,.0f}  |  Risk/trade: {RISK_PER_TRADE*100:.0f}%\n\n"

    for i, r in enumerate(results[:TOP_N], 1):

        row = (
            f"{'─'*40}\n"
            f"#{i}  <b>{r['symbol']}</b>  {r['signal']}\n"
            f"Price      : Rp {r['price']:,.0f}\n"
            f"Score      : {r['score']:.3f}\n"
            f"ML Prob    : {r['ml_prob']:.3f}\n"
            f"Sentiment  : {r['raw_sent']:+.3f}  (norm {r['sentiment']:.3f})\n"
            f"Risk Score : {r['risk_score']:.2f}\n"
            f"Stop Loss  : Rp {r['stop_loss']:,.0f}\n"
            f"Take Profit: Rp {r['take_profit']:,.0f}\n"
            f"R:R Ratio  : 1 : {r['risk_reward']}\n"
            f"Shares     : {r['shares']:,}\n"
            f"Capital    : Rp {r['capital_used']:,.0f}\n\n"
        )

        print(row)
        message += row

    message += f"\nScanned {len(stocks)} stocks  |  Valid signals: {len(results)}"

    send(message)
    print("\n✅ Telegram notification sent.")
    print("Done.\n")


if __name__ == "__main__":
    run()