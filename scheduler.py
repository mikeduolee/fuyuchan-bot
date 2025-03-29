import time
from dotenv import load_dotenv
import os
from linebot import LineBotApi
from linebot.models import TextSendMessage
from utils import get_daily_rune, load_all_users

load_dotenv()
line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))

def push_daily_rune():
    users = load_all_users()
    message = get_daily_rune()
    for user_id in users:
        try:
            line_bot_api.push_message(user_id, TextSendMessage(text=message))
        except Exception as e:
            print(f"❌ 推播失敗: {user_id} - {str(e)}")

if __name__ == "__main__":
    while True:
        current_time = time.strftime("%H:%M")
        if current_time == "08:00":
            print("🌞 符語娘準備發送今日符文中...")
            push_daily_rune()
            time.sleep(60)
        else:
            time.sleep(30)
