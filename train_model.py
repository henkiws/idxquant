from data.idx_list import get_idx_stocks
from data.fetch_stock import get_stock
from indicators.technical import add_indicators
import pandas as pd

from ml.train import train


print("Starting IDX training...")

stocks = get_idx_stocks()

print(f"Total stocks: {len(stocks)}")

dfs = []

for s in stocks:

    print(f"\nFetching: {s}")

    try:

        df = get_stock(s)

        if df is None:
            print("FAILED: df is None")
            continue

        if df.empty:
            print("FAILED: df empty")
            continue

        print(f"Downloaded rows: {len(df)}")

        df = add_indicators(df)

        if df is None or df.empty:
            print("FAILED: indicators empty")
            continue

        print(f"Indicators rows: {len(df)}")

        dfs.append(df)

        print("SUCCESS")

    except Exception as e:

        print(f"ERROR: {e}")


print("\nFinished fetching.")

print(f"Valid dataframes: {len(dfs)}")


if len(dfs) == 0:

    print("❌ NO DATA. Cannot train.")
    exit()


combined = pd.concat(dfs, ignore_index=True)

print(f"Combined rows: {len(combined)}")

# =====================================
# HEDGE FUND LEVEL COLUMN CLEANING FIX
# =====================================

# flatten multi-index columns if exist
if isinstance(combined.columns, pd.MultiIndex):
    combined.columns = combined.columns.get_level_values(0)

# remove duplicate columns (KEEP FIRST ONLY)
combined = combined.loc[:, ~combined.columns.duplicated(keep="first")]

# force Close to be Series
close_col = combined["Close"]

# if still DataFrame, take first column
if isinstance(close_col, pd.DataFrame):
    close_col = close_col.iloc[:, 0]

# assign back clean Close
combined["Close"] = pd.Series(close_col).astype(float)

# remove invalid rows
combined = combined.dropna(subset=["Close"])

# reset index
combined = combined.reset_index(drop=True)

# FINAL DEBUG CHECK
print("\nFINAL CLEAN CHECK:")
print("Close type:", type(combined["Close"]))
print("Columns count:", len(combined.columns))
print("Shape:", combined.shape)

# =====================================

train(combined)

print("✅ TRAINING COMPLETE")