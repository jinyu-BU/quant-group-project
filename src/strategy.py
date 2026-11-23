import pandas as pd

def double_ma_strategy(df: pd.DataFrame, short_window=5, long_window=20):
    """
    双均线策略：短期均线上穿长期均线（金叉）持仓，下穿（死叉）空仓
    """
    df = df.copy()
    df["ma_short"] = df["close"].rolling(window=short_window).mean()
    df["ma_long"] = df["close"].rolling(window=long_window).mean()

    # 持仓状态：短均线在长均线上方 => 1，否则 => 0
    df["signal"] = (df["ma_short"] > df["ma_long"]).astype(int)
    
    # 均线未形成的前几天，signal 置 0
    df.loc[df["ma_long"].isna(), "signal"] = 0

    return df