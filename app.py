from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

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
    msg = event.message.text.lower()
    if "抽盧恩" in msg or "/draw" in msg:
        reply = "🪄 你抽到的符文是：Wunjo（喜悅）！今天適合放鬆與感恩～"
    elif "感情占卜" in msg or "/love" in msg:
        reply = "💗 抽到 Thurisaz（逆位）：提醒你暫時觀察彼此的情緒，不用急著突破～"
    else:
        reply = "嗨～我是符語娘 FuYu-chan！你可以對我說「抽盧恩」、「感情占卜」來看看今日的能量訊息 🧝‍♀️✨"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

if __name__ == "__main__":
    app.run()
