from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv
import os
from utils import get_daily_rune, get_three_runes, get_learning_rune, add_user_if_new

load_dotenv()
app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))

@app.route("/callback", methods=['POST'])
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
    user_id = event.source.user_id
    add_user_if_new(user_id)
    msg = event.message.text.strip()
    if "三符文" in msg:
        reply = get_three_runes()
    elif "每日練習" in msg:
        reply = get_learning_rune()
    elif "抽符文" in msg or "占卜" in msg:
        reply = get_daily_rune()
    else:
        reply = (
            "🔮 符語娘悄悄說：\n\n"
            "你好呀，我是符語娘，一位與盧恩符文共鳴的小靈語師🌙\n"
            "我每天會替你抽出一枚古老符文，傳遞宇宙的訊息～\n\n"
            "你可以對我說：\n"
            "✨ 抽符文｜📜 三符文占卜｜🧘‍♀️ 每日練習\n\n"
            "在心中想好問題，再輕聲喚我吧～🪄"
        )
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
