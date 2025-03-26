import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
user_id = os.getenv("LINE_USER_ID")

@app.route("/webhook", methods=["GET", "POST"])
def callback():
    if request.method == "GET":
        return "FuYu-chan webhook ready 💫", 200

    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text.strip() == "抽盧恩":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="今日盧恩：🌟 Fehu（行動＋財富）")
        )

# 自動推播任務
def daily_push():
    now = datetime.now(pytz.timezone("Asia/Taipei"))
    msg = f"🧙‍♀️ FuYu-chan 今日盧恩：Eiwaz（轉化・堅持）\n時間：{now.strftime('%Y-%m-%d %H:%M')}"
    line_bot_api.push_message(user_id, TextSendMessage(text=msg))

scheduler = BackgroundScheduler()
scheduler.add_job(daily_push, 'cron', hour=8, minute=0, timezone='Asia/Taipei')
scheduler.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)