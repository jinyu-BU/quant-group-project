from src.data_loader import get_index_data
from src.strategy import double_ma_strategy
from src.backtest import run_backtest
from src.plot_result import plot_net_curve
import pandas as pd

if __name__ == "__main__":
    print("1. 开始获取数据...")
    df_all = get_index_data(
        symbol="sh000300",
        start_date="2015-01-01",
        end_date="2024-12-31",
        save_path="./data/hs300.csv"
    )
    df_all["date"] = pd.to_datetime(df_all["date"])

    # 划分样本内 (2015-2020) 和 样本外 (2021-2024)
    df_in = df_all[df_all["date"] <= pd.Timestamp("2020-12-31")].copy()
    df_out = df_all[df_all["date"] > pd.Timestamp("2020-12-31")].copy()

    print("\n2. 开始样本内回测 (2015-2020)...")
    df_in = double_ma_strategy(df_in, short_window=5, long_window=20)
    df_in_res, metric_in_strat, metric_in_bench = run_backtest(df_in)
    print("========【样本内指标】========")
    print("策略指标：", metric_in_strat)
    print("基准指标：", metric_in_bench)

    print("\n3. 开始样本外回测 (2021-2024)...")
    df_out = double_ma_strategy(df_out, short_window=5, long_window=20)
    df_out_res, metric_out_strat, metric_out_bench = run_backtest(df_out)
    print("========【样本外指标】========")
    print("策略指标：", metric_out_strat)
    print("基准指标：", metric_out_bench)

    print("\n4. 正在生成净值图表...")
    df_total = pd.concat([df_in_res, df_out_res], ignore_index=True)
    plot_net_curve(df_total)
    print("全部运行完毕！")