"""
SINGLE SOURCE OF TRUTH for ML features.
Both train.py and predict.py import from here.
"""

FEATURES = [
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