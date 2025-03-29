
import os
import random
import json
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

with open('runes.json', encoding='utf-8') as f:
    runes = json.load(f)

def get_random_rune():
    rune = random.choice(runes)
    reversed_flag = random.random() < 0.5
    position = "逆位" if reversed_flag else "正位"
    meaning = rune["reversed"] if reversed_flag else rune["upright"]
    return rune["symbol"], rune["name"], position, meaning

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
    text = event.message.text

    if "抽一張" in text:
        symbol, name, position, meaning = get_random_rune()
        reply = f"🙋‍♀️你抽到了：{symbol}（{name}）\n{position}｜💡 心靈指引：{meaning['spiritual']}\n🚀 行動建議：{meaning['action']}"
    elif "抽三張" in text:
        reply = ""
        for i in range(3):
            symbol, name, position, meaning = get_random_rune()
            reply += f"第{i+1}張：{symbol}（{name}）\n{position}｜💡{meaning['spiritual']}\n🚀{meaning['action']}\n\n"
    elif "感情" in text:
        symbol, name, position, meaning = get_random_rune()
        reply = f"💖 感情牌抽出：{symbol}（{name}）\n{position}｜💗 情感啟示：{meaning['love']}\n📌 行動提醒：{meaning['loveAction']}"
    else:
        reply = "輸入「抽一張」「抽三張」或「感情抽牌」來試試看吧～ ✨"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    app.run()
