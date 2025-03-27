from flask import Flask, request

app = Flask(__name__)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    return "FuYu-chan webhook ready 💫"

if __name__ == "__main__":
    app.run(debug=True, port=8080)
