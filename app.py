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

    if user_message in ["骰", "骰盧恩", "骰一顆", "骰三顆盧恩"]:
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

    elif user_message in ["骰三顆", "三顆盧恩", "三顆"]:
        runes = runes_df.sample(3).reset_index(drop=True)
        positions = ["過去", "現在", "未來"]
        result_text = "🔮 三顆盧牌符文解讀：\n\n"

        for i in range(3):
            rune = runes.iloc[i]
            is_reversed = random.choice([True, False])
            if is_reversed:
                meaning = rune["meaning_reversed"]
                guidance = rune["guidance_reversed"]
                position = "逆位"
            else:
                meaning = rune["meaning_upright"]
                guidance = rune["guidance_upright"]
                position = "正位"

            result_text += f"{positions[i]}：{rune['name']}（{position}）\n意義：{meaning}\n指引語：{guidance}\n\n"

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result_text.strip()))

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="使用方式不對喔~\n使用方式：\n心中想好要問的問題，\n再輸入"骰盧恩", "骰一顆" 或 "骰三顆盧恩"，\n請再重新輸入一次 😊")
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
