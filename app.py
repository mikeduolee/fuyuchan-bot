from flask import Flask, request, abort
from apscheduler.schedulers.background import BackgroundScheduler
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import random
import os
import json
import datetime
import pytz

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

with open("data/spreads.json", "r") as f:
    spreads = json.load(f)

with open("data/moon_phases.json", "r") as f:
    moon_data = json.load(f)

with open("data/rune_messages.json", "r", encoding="utf-8") as f:
    rune_messages = json.load(f)

runes = list(rune_messages.keys())

def get_daily_rune():
    rune = random.choice(runes)
    is_reversed = random.choice([True, False])
    position = "reversed" if is_reversed else "upright"
    meanings = rune_messages.get(rune, {}).get(position, ["靈感降臨中...", "敬請期待完整解讀✨"])
    img_url = f"https://your.cdn.url/runes/{rune}_{position}.png"
    return rune, position, meanings, img_url

def send_daily_rune():
    user_id = os.getenv("LINE_USER_ID")
    if not user_id:
        return
    rune, position, meanings, img_url = get_daily_rune()
    today = datetime.datetime.now(pytz.timezone("Asia/Taipei")).strftime("%Y/%m/%d")

    messages = [
        TextSendMessage(text=f"🌞 {today} 的每日符語來囉！"),
        TextSendMessage(text=f"🔮 今日符文：{rune}（{'逆位' if position == 'reversed' else '正位'}）"),
        TextSendMessage(text=f"💭 心靈指引：{meanings[0]}\n🔧 行動建議：{meanings[1]}"),
        TextSendMessage(text=img_url)
    ]
    line_bot_api.push_message(user_id, messages)

scheduler = BackgroundScheduler(timezone="Asia/Taipei")
scheduler.add_job(send_daily_rune, 'cron', hour=8, minute=0)
scheduler.start()

@app.route("/webhook", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text.lower()
    if "抽盧恩" in msg:
        rune, position, meanings, img_url = get_daily_rune()
        reply = [
            TextSendMessage(text=f"🔮 抽到的是 {rune}（{'逆位' if position == 'reversed' else '正位'}）"),
            TextSendMessage(text=f"💭 心靈指引：{meanings[0]}\n🔧 行動建議：{meanings[1]}"),
            TextSendMessage(text=img_url)
        ]
        line_bot_api.reply_message(event.reply_token, reply)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="✨ FuYu-chan 隨時待命，要來抽盧恩嗎？"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
