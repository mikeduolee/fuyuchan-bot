
import random
import pandas as pd
from linebot import LineBotApi
from linebot.models import TextSendMessage
import os

def push_daily_practice_fuyu():
    line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
    user_list_file = "user_ids.json"

    # 讀取使用者清單
    if not os.path.exists(user_list_file):
        print("未找到使用者清單，跳過推播")
        return

    with open(user_list_file, "r") as f:
        users = json.load(f)

    # 讀取每日練習資料
    df = pd.read_csv("fuyu_rune_readings_final_upgraded.csv")
    today_row = df.sample(1).iloc[0]

    rune = today_row["符文名稱"]
    position = today_row["正逆位"]
    keyword = today_row["關鍵字"]
    intro = today_row["解釋語句"]
    guidance = today_row["心靈指引"]
    action = today_row["行動建議"]

    # 組合推播訊息
    message = (
        f"🧘‍♀️ 符語娘每日練習：

"
        f"✨ 今日符文：{rune}（{position}）
🔑 關鍵字：{keyword}

"
        f"📖 指引語：{intro}

"
        f"🌙 心靈引導：
{guidance}

"
        f"📌 行動建議：
{action}"
    )

    for uid in users:
        try:
            line_bot_api.push_message(uid, TextSendMessage(text=message))
        except Exception as e:
            print(f"❌ 推播失敗：{uid}, 錯誤：{e}")
