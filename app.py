from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import json
import random

app = Flask(__name__)

# 設定 LINE BOT API 金鑰與 handler secret
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# 載入盧恩資料
with open("fuyu_rune_data_v7.json", "r", encoding="utf-8") as f:
    rune_data = json.load(f)

def draw_rune():
    rune_key = random.choice(list(rune_data.keys()))
    return rune_data[rune_key]

def draw_three_runes():
    keys = random.sample(list(rune_data.keys()), 3)
    return [(["過去", "現在", "未來"][i], rune_data[k]) for i, k in enumerate(keys)]

@app.route("/webhook", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text.strip()

    if "骰盧恩" in msg or "抽一張" in msg:
        rune = draw_rune()
        reply_text = f"🔮 今日符文：{rune['name']}（{rune['position']}）\n\n{rune['meaning']}\n\n✨ 指引語：{rune['guidance']}"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

    elif "骰三顆" in msg or "抽三張" in msg:
        runes = draw_three_runes()
        messages = []
        for position, rune in runes:
            text = f"🔮【{position}】{rune['name']}（{rune['position']}）\n\n{rune['meaning']}\n\n✨ 指引語：{rune['guidance']}"
            messages.append(TextSendMessage(text=text[:4800]))  # 安全留 buffer
        line_bot_api.reply_message(event.reply_token, messages)

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="使用方式不對喔～請輸入：\n🔮『骰盧恩』 or 『骰三張』來獲得今日符語娘的祝福 ✨")
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)