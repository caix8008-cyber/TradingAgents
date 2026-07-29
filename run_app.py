import os
import requests
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.graph.trading_graph import TradingAgentsGraph

SERVERCHAN_SENDKEY = os.getenv("SERVERCHAN_SENDKEY")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY")

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
    if not DEEPSEEK_KEY:
        print("【嚴重錯誤】未讀取到 DEEPSEEK_API_KEY！請檢查 GitHub Secrets。")
        exit(1)

    print("【成功】已讀取 DEEPSEEK_API_KEY，啟動 DeepSeek 引擎...")

    # 套件會自動讀取環境變數中的 TRADINGAGENTS_LLM_PROVIDER="deepseek"
    ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG)

    try:
        decision = ta.propagate("NVDA", "2024-05-10")
        print("AI 決策結果：", decision)

        send_wechat(
            title="TradingAgents AI 股票決策報告",
            content=f"### NVDA 分析報告\n```json\n{decision}\n```"
        )
    except Exception as e:
        print(f"【執行失敗】呼叫模型時發生錯誤: {e}")
