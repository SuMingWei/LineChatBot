import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ButtonsTemplate,ImageSendMessage,CarouselTemplate,CarouselColumn


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


def send_button_message(reply_token, title, text, btn, url):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text='button template',
        template = ButtonsTemplate(
            title = title,
            text = text,
            thumbnail_image_url = url,
            actions = btn
        )
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"

def send_carousel_button_message(reply_token,title,text,url,btn1,btn2,btn3,btn4,btn5):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url=url,
                    title=title,
                    text=text,
                    actions=btn1
                ),
                CarouselColumn(
                    thumbnail_image_url=url,
                    title=title,
                    text=text,
                    actions=btn2
                ),
                CarouselColumn(
                    thumbnail_image_url=url,
                    title=title,
                    text=text,
                    actions=btn3
                ),
                CarouselColumn(
                    thumbnail_image_url=url,
                    title=title,
                    text=text,
                    actions=btn4
                ),
                CarouselColumn(
                    thumbnail_image_url=url,
                    title=title,
                    text=text,
                    actions=btn5
                )
            ]
        )
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"

def send_image_message(reply_token, url):
    line_bot_api = LineBotApi(channel_access_token)
    message = ImageSendMessage(
        original_content_url = url,
        preview_image_url = url
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"

