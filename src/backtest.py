import pandas as pd
import numpy as np

def calc_metrics(net_series: pd.Series, rf=0.025):
    """
    计算回测指标：累计收益率、年化收益率、最大回撤、夏普比率
    """
    total_return = net_series.iloc[-1] - 1
    days = len(net_series)
    annual_return = net_series.iloc[-1] ** (252.0 / days) - 1

    # 最大回撤
    rolling_max = net_series.cummax()
    drawdown = (net_series - rolling_max) / rolling_max
    max_drawdown = drawdown.min()

    # 夏普比率（稳健写法）
    daily_return = net_series.pct_change().dropna()
    excess_daily = daily_return - rf / 252
    if excess_daily.std() == 0:
        sharpe = 0
    else:
        sharpe = excess_daily.mean() / excess_daily.std() * np.sqrt(252)

    return {
        "累计收益率": round(total_return, 4),
        "年化收益率": round(annual_return, 4),
        "最大回撤": round(max_drawdown, 4),
        "夏普比率": round(sharpe, 4)
    }

def run_backtest(df: pd.DataFrame, initial_capital=100000, fee_rate=0.0003):
    """
    执行回测
    """
    df = df.reset_index(drop=True).copy()
    
    # 关键：T日收盘后产生信号，T+1日执行（避免前视偏差）
    df["signal_exec"] = df["signal"].shift(1).fillna(0).astype(int)

    capital = initial_capital
    position = 0
    net_list = []
    base_net_list = []
    base_price_start = df["close"].iloc[0]

    for idx, row in df.iterrows():
        price = row["close"]
        sig = row["signal_exec"]

        # 买入
        if sig == 1 and position == 0:
            buy_money = capital * (1 - fee_rate)
            position = buy_money / price
            capital = 0
        # 卖出
        elif sig == 0 and position > 0:
            sell_income = position * price * (1 - fee_rate)
            capital = sell_income
            position = 0

        # 记录每日净值
        total_asset = capital + position * price
        net_list.append(total_asset / initial_capital)
        base_net_list.append(price / base_price_start)

    df["strategy_net"] = net_list
    df["benchmark_net"] = base_net_list

    strat_metric = calc_metrics(df["strategy_net"])
    bench_metric = calc_metrics(df["benchmark_net"])
    return df, strat_metric, bench_metric