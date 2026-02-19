"""
Run this ONCE before running main.py:
    python train_model.py
"""

import pandas as pd

from data.idx_list import get_idx_stocks
from data.fetch_stock import get_stock
from indicators.technical import add_indicators
from ml.train import train


def main():
    print("="*60)
    print("  IDXQuantBot — Model Training")
    print("="*60 + "\n")

    stocks = get_idx_stocks()
    print(f"Fetching data for {len(stocks)} stocks...\n")

    dfs = []

    for symbol in stocks:
        print(f"  {symbol}...", end=" ")
        try:
            df = get_stock(symbol)
            if df is None or df.empty:
                print("SKIP (no data)")
                continue

            df = add_indicators(df)
            if df is None or df.empty:
                print("SKIP (indicators failed)")
                continue

            print(f"OK  ({len(df)} rows)")
            dfs.append(df)

        except Exception as e:
            print(f"ERROR ({e})")

    print(f"\nValid dataframes: {len(dfs)}")

    if not dfs:
        print("❌ No data collected. Cannot train.")
        return

    # ── Combine all stock data ────────────────────────────────────────────────
    combined = pd.concat(dfs, ignore_index=True)

    # flatten MultiIndex just in case concat reintroduces it
    if isinstance(combined.columns, pd.MultiIndex):
        combined.columns = combined.columns.get_level_values(0)

    # remove duplicate columns
    combined = combined.loc[:, ~combined.columns.duplicated(keep="first")]

    # force Close to clean float Series
    close = combined["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    combined["Close"] = pd.Series(close).astype(float)

    combined = combined.dropna(subset=["Close"])
    combined = combined[combined["Close"] > 0]
    combined = combined.reset_index(drop=True)

    print(f"\nCombined dataset: {combined.shape[0]:,} rows × {combined.shape[1]} columns")

    # ── Train ─────────────────────────────────────────────────────────────────
    train(combined)

    print("\n✅ TRAINING COMPLETE")
    print("Model saved to: models/model.pkl")
    print("You can now run: python main.py\n")


if __name__ == "__main__":
    main()