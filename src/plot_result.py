import matplotlib.pyplot as plt
import pandas as pd

def plot_net_curve(df: pd.DataFrame, save_img_path="./net_curve.png"):
    # 设置中文字体，防止图表里的中文变成方块
    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
    plt.rcParams["axes.unicode_minus"] = False
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["date"], df["strategy_net"], label="双均线策略", linewidth=1.2)
    ax.plot(df["date"], df["benchmark_net"], label="沪深300(基准)", linewidth=1.2)
    
    ax.set_title("策略与基准归一化净值对比")
    ax.set_xlabel("日期")
    ax.set_ylabel("净值(初始=1.0)")
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(save_img_path, dpi=150)
    plt.close()
    print(f"\n净值图已保存至 {save_img_path}")