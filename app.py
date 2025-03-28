
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
import os
import random
import pandas as pd

app = Flask(__name__)

# 設定 LINE BOT API 金鑰與 handler secret
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# 載入盧恩資料集
runes_df = pd.read_csv("runes_data_v7.csv")

@app.route("/", methods=['GET'])
def home():
    return "FuYu-chan is running!"

@app.route("/webhook", methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip()

    if user_message in ["抽", "抽盧恩", "抽一張", "抽一張盧恩"]:
        rune = runes_df.sample(1).iloc[0]
        is_reversed = random.choice([True, False])

        if is_reversed:
            image_url = rune["image_reversed"]
            meaning = rune["meaning_reversed"]
            guidance = rune["guidance_reversed"]
            position = "逆位"
        else:
            image_url = rune["image_upright"]
            meaning = rune["meaning_upright"]
            guidance = rune["guidance_upright"]
            position = "正位"

        messages = [
            ImageSendMessage(original_content_url=image_url, preview_image_url=image_url),
            TextSendMessage(text=f"🔮 盧恩符文：{rune['name']}（{position}）\n\n意義：{meaning}"),
            TextSendMessage(text=f"✨ 指引語：{guidance}")
        ]
        line_bot_api.reply_message(event.reply_token, messages)

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="感謝您的訊息！\n很抱歉，本帳號無法回覆用戶的訊息。\n敬請期待我們下次發送的內容喔 😊")
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
