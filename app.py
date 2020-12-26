import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message,send_image_message

load_dotenv()

machine = TocMachine(
    states=[
        "user", 
        "choose_area",
        "choose_region", 
        "choose_restaurant",
        "recommand_restaurant",
        "recommand_menu"
    ],
    transitions=[
        {"trigger": "advance","source": "user","dest": "choose_area","conditions": "is_going_to_choose_area"},
        {"trigger": "advance","source": "choose_area","dest": "choose_region","conditions": "is_going_to_choose_region"},
        {"trigger": "advance","source": "choose_region","dest": "choose_restaurant","conditions": "is_going_to_choose_restaurant"},
        {"trigger": "advance","source": "choose_region","dest": "choose_area","conditions": "is_going_to_choose_area"},
        {"trigger": "advance","source": "choose_restaurant","dest": "recommand_restaurant","conditions": "is_going_to_recommand_restaurant"},
        {"trigger": "advance","source": "choose_restaurant","dest": "choose_region","conditions": "is_going_to_choose_region"},
        {"trigger": "advance","source": "recommand_restaurant","dest": "recommand_menu","conditions": "is_going_to_recommand_menu"},
        {"trigger": "advance","source": "recommand_restaurant","dest": "recommand_restaurant","conditions": "is_going_to_recommand_restaurant"},
        {"trigger": "advance","source": "recommand_menu","dest": "recommand_restaurant","conditions": "is_going_to_recommand_restaurant"},
        {
            "trigger": "go_back",
            "source": [
                "choose_area",
                "choose_region", 
                "choose_restaurant",
                "recommand_restaurant",
                "recommand_menu"
            ], 
            "dest": "user"
        },
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            if event.message.text.lower() == 'fsm':
                send_image_message(event.reply_token, 'https://i.ibb.co/YdjDk6w/fsm.png?')
            elif machine.state != 'user' and event.message.text.lower() == 'restart':
                send_text_message(event.reply_token, '輸入『aneater』即可開始使用。\n隨時輸入『restart』可以從頭開始。\n隨時輸入『fsm』可以得到當下的狀態圖。')
                machine.go_back()
            elif machine.state == "user":
                send_text_message(event.reply_token, '輸入『aneater』即可開始使用。\n隨時輸入『restart』可以從頭開始。\n隨時輸入『fsm』可以得到當下的狀態圖。')
            elif machine.state == "choose_area":
                text = '請選擇一個區域：\n\n若是台北、新北、桃園、基隆地區請輸入『北部』。\n'
                text += '若是新竹、苗栗、台中、南投地區請輸入『北中部』。\n'
                text += '若是彰化、雲林、嘉義、台南地區請輸入『中南部』。\n'
                text += '若是高雄、屏東、金門、澎湖地區請輸入『南部及外島』。\n'
                text += '若是宜蘭、花蓮、台東地區請輸入『東部』。\n'        
                send_text_message(event.reply_token, text)
            elif machine.state == "choose_region":
                send_text_message(event.reply_token, '選擇一個城市，或輸入『重新選擇地區』')
            elif machine.state == "choose_restaurant":
                send_text_message(event.reply_token, '選擇『推薦餐廳』或是『重新選擇城市』！')
            elif machine.state == "recommand_restaurant":
                send_text_message(event.reply_token, '選擇『前往訂餐』或是『快速瀏覽菜單』或是『其他推薦餐廳』')
            elif machine.state == "recommand_menu":
                send_text_message(event.reply_token, "選擇『其他推薦餐廳』或是輸入『restart』重新開始")
            
    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
    
