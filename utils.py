import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ButtonsTemplate,ImageSendMessage,CarouselTemplate,CarouselColumn,URITemplateAction,MessageTemplateAction


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

def send_carousel_button_message(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Tapei.jpg',
                    title='請選擇一個區域',
                    text='包含台北、新北、桃園、基隆地區',
                    actions=[
                        MessageTemplateAction(
                            label='北部',
                            text='北部'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Taichung.jpg',
                    title='請選擇一個區域',
                    text='包含新竹、苗栗、台中、南投地區',
                    actions=[
                        MessageTemplateAction(
                            label='北中部',
                            text='北中部'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Tainan.jpg',
                    title='請選擇一個區域',
                    text='包含彰化、雲林、嘉義、台南地區',
                    actions=[
                        MessageTemplateAction(
                            label='中南部',
                            text='中南部'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Kaohsiung.jpg',
                    title='請選擇一個區域',
                    text='包含高雄、屏東、金門、澎湖地區',
                    actions=[
                        MessageTemplateAction(
                            label='南部及外島',
                            text='南部及外島'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Yilan.jpg',
                    title='請選擇一個區域',
                    text='包含宜蘭、花蓮、台東地區',
                    actions=[
                        MessageTemplateAction(
                            label='東部',
                            text='東部'
                        )
                    ]
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

