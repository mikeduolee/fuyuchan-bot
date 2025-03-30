
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import pandas as pd
import random

def handle_daily_practice_event(event, line_bot_api):
    if event.message.text.strip() == "每日練習":
        df = pd.read_csv("fuyu_rune_readings_final_upgraded.csv")
        today_row = df.sample(1).iloc[0]

        rune = today_row["符文名稱"]
        position = today_row["正逆位"]
        keyword = today_row["關鍵字"]
        intro = today_row["解釋語句"]
        guidance = today_row["心靈指引"]
        action = today_row["行動建議"]

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

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )
