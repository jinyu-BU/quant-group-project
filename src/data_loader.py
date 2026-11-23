import akshare as ak
import pandas as pd
import os

def get_index_data(symbol: str, start_date: str, end_date: str, save_path: str):
    """
    获取指数日线数据
    """
    print(f"正在下载 {symbol} 的数据，请稍候...")
    
    # 使用更新后的新浪接口
    df = ak.index_zh_daily_sina(symbol=symbol)
    
    # 转换日期格式并筛选
    df["date"] = pd.to_datetime(df["date"])
    df = df[(df["date"] >= pd.Timestamp(start_date)) & 
            (df["date"] <= pd.Timestamp(end_date))].copy()
            
    df = df.reset_index(drop=True)
    
    # 确保保存路径存在
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    # 保存为csv文件
    df.to_csv(save_path, index=False, encoding="utf-8-sig")
    print(f"数据已保存至 {save_path}, 共 {len(df)} 行")
    return df

if __name__ == "__main__":
    # 测试获取沪深300的数据
    get_index_data(
        symbol="sh000300",
        start_date="2015-01-01",
        end_date="2024-12-31",
        save_path="./data/hs300.csv"
    )