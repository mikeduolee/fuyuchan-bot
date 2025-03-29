from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
import os
import json
import random

app = Flask(__name__)

# LINE Channel 金鑰
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
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text

    if "骰盧恩" in msg or "抽一張" in msg:
        rune = draw_rune()
        messages = [
            TextSendMessage(text=rune["description"]),
            ImageSendMessage(original_content_url=rune["image"],
                             preview_image_url=rune["image"])
        ]
        line_bot_api.reply_message(event.reply_token, messages)

    elif "骰三顆" in msg or "抽三張" in msg:
        runes = draw_three_runes()
        descriptions = []
        for position, rune in runes:
            desc = f"【{position}】\n" + rune["description"]
            descriptions.append(desc)
        full_text = "\n\n".join(descriptions)
        images = [ImageSendMessage(original_content_url=r["image"], preview_image_url=r["image"]) for _, r in runes]
        messages = [TextSendMessage(text=full_text)] + images
        line_bot_api.reply_message(event.reply_token, messages)

    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessageTextSendMessage(text="""🔮 符語娘悄悄說：

你可以這樣跟我互動：
✨ 「抽符文」—— 抽出今日專屬符文與指引  
📜 「三符文占卜」—— 展開一場更完整的占卜解析  

在心中想好問題，再悄悄對我說一聲，我就會為你揭開符文的語言之門🪄""")
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
