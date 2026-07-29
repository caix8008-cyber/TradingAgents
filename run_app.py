import os
import requests
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.graph.trading_graph import TradingAgentsGraph

SERVERCHAN_SENDKEY = os.getenv("SERVERCHAN_SENDKEY")
DEEPSEEK_KEY = os.getenv("OPENAI_API_KEY")

def send_wechat(title, content):
    if not SERVERCHAN_SENDKEY:
        print("【警告】未設定 SERVERCHAN_SENDKEY，跳過微信推送")
        return
    url = f"https://sctapi.ftqq.com/{SERVERCHAN_SENDKEY}.send"
    payload = {"title": title, "desp": content}
    try:
        requests.post(url, data=payload)
        print("【成功】微信推送已發送！")
    except Exception as e:
        print(f"【錯誤】推送失敗: {e}")

if __name__ == "__main__":
    # 檢查 API Key 是否有正確傳入
    if not DEEPSEEK_KEY:
        print("【嚴重錯誤】沒有偵測到 DEEPSEEK_API_KEY！請檢查 GitHub Secrets 設定。")
        exit(1)
    else:
        print("【成功】已成功讀取 DeepSeek API Key，開始執行 AI 分析...")

    # 初始化專案配置
    config = DEFAULT_CONFIG.copy()
    ta = TradingAgentsGraph(debug=True, config=config)

    # 執行 AI 分析
    try:
        decision = ta.propagate("NVDA", "2024-05-10")
        print("AI 決策結果：", decision)

        # 發送微信通知
        send_wechat(
            title="TradingAgents AI 股票決策報告", 
            content=f"### NVDA 分析報告\n```json\n{decision}\n```"
        )
    except Exception as e:
        print(f"【執行失敗】呼叫模型時發生錯誤: {e}")
