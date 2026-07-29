import os
import requests
from datetime import datetime
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.graph.trading_graph import TradingAgentsGraph

# 1. 讀取環境變數 (Secrets 裡面設的金鑰)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
SERVERCHAN_SENDKEY = os.getenv("SERVERCHAN_SENDKEY")

def send_wechat(title, content):
    """將分析結果推送到微信"""
    if not SERVERCHAN_SENDKEY:
        print("未偵測到 SERVERCHAN_SENDKEY，跳過微信推送")
        return
    url = f"https://sctapi.ftqq.com/{SERVERCHAN_SENDKEY}.send"
    payload = {
        "title": title,
        "desp": content
    }
    try:
        requests.post(url, data=payload)
        print("微信推送完成！")
    except Exception as e:
        print(f"推送失敗: {e}")

# 2. 修改模型與 API 配置
config = DEFAULT_CONFIG.copy()

# 如果專案支援 DeepSeek，可以在這裡指定 Provider 與 API Key
# (若專案是吃環境變數，它會自動抓取 DEEPSEEK_API_KEY)
if DEEPSEEK_API_KEY:
    config["api_key"] = DEEPSEEK_API_KEY
    # config["llm_provider"] = "deepseek" # 如果該套件支援 deepseek 參數可在此指定

# 3. 初始化 AI 交易代理人
ta = TradingAgentsGraph(debug=True, config=config)

if __name__ == "__main__":
    # ==================== 可自行修改的參數 ====================
    stock_symbol = "NVDA"  # 想分析的股票代碼 (例如: NVDA, AAPL, TSLA)
    target_date = datetime.now().strftime("%Y-%m-%d")  # 自動抓取今天日期，也可以寫死如 "2024-05-10"
    # =========================================================

    print(f"開始分析股票：{stock_symbol} (日期: {target_date})...")

    try:
        # 4. 讓 AI 執行推導決策
        decision = ta.propagate(stock_symbol, target_date)
        print("AI 決策結果：", decision)

        # 5. 將結果發送到微信
        push_title = f"AI 股票交易決策：{stock_symbol}"
        push_content = f"### 分析標的：{stock_symbol}\n**分析日期**：{target_date}\n\n**AI 決策報告**：\n```json\n{decision}\n```"
        
        send_wechat(push_title, push_content)

    except Exception as e:
        print(f"執行過程發生錯誤: {e}")
