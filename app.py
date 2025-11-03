<<<<<<< HEAD
from flask import Flask, request, abort
from linebot.v3.messaging import MessagingApi, Configuration
from linebot.v3.webhook import WebhookHandler
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.models.message import TextMessage

app = Flask(__name__)

# あなたのチャネルアクセストークンとチャネルシークレットをセット
LINE_CHANNEL_ACCESS_TOKEN = "U3eef45f995095143c4a901c68a43dfc5"
LINE_CHANNEL_SECRET = "925620ad909aba8737e56c2b808ffb84"

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
line_bot_api = MessagingApi(configuration=configuration)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except Exception:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent):
    reply_token = event.reply_token
    user_message = event.message.text

    line_bot_api.reply_message(
        reply_token=reply_token,
        messages=[TextMessage(text=f"あなたのメッセージ: {user_message}")]
    )

if __name__ == "__main__":
    app.run(port=5000)
=======
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return "こんにちはこれはスマホでも開けるWebアプリです"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
>>>>>>> c4d3048 (初回アップロード)
