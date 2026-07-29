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
    if not DEEPSEEK_KEY:
        print("【嚴重錯誤】沒有偵測到 DEEPSEEK_API_KEY！請檢查 GitHub Secrets 設定。")
        exit(1)
    
    print("【成功】已成功讀取 DeepSeek API Key，開始指定 DeepSeek 模型...")

    # 複製預設配置並強制修改模型名稱為 deepseek-chat
    config = DEFAULT_CONFIG.copy()
    config["quick_think_llm"] = "deepseek-chat"
    config["deep_think_llm"] = "deepseek-chat"

    # 初始化交易代理人
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
