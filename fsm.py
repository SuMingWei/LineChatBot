from transitions.extensions import GraphMachine

from utils import send_text_message,send_button_message,send_carousel_button_message

from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction,CarouselColumn
import pandas as pd
import random
# global variable
area = ''
region = ''
restaurant_id = -1
restaurant_url = ''

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    # start on user
    def is_going_to_choose_area(self,event):
        text = event.message.text
        if(text.lower() == 'aneater') or (self.state == 'choose_region' and text == '重新選擇地區'):
            return True

        return False

    def on_enter_choose_area(self,event):
        text = '請選擇一個區域：\n\n若是想選擇台北、新北、桃園、基隆地區請輸入『北部』。\n'
        text += '若是想選擇新竹、苗栗、台中、南投地區請輸入『北中部』。\n'
        text += '若是想選擇彰化、雲林、嘉義、台南地區請輸入『中南部』。\n'
        text += '若是想選擇高雄、屏東、金門、澎湖地區請輸入『南部及外島』。\n'
        text += '若是想選擇宜蘭、花蓮、台東地區請輸入『東部』。\n'
        
        send_text_message(event.reply_token, text)

    def is_going_to_choose_region(self,event):
        global area
        text = event.message.text

        if text == '北部':
            area = '北部'
            return True
        elif text == '北中部':
            area = '北中部'
            return True
        elif text == '中南部':
            area = '中南部'
            return True
        elif text == '南部及外島':
            area = '南部及外島'
            return True
        elif text == '東部':
            area = '東部'
            return True
        elif (self.state == 'choose_restaurant' and text == '重新選擇城市'):
            return True

        return False

    def on_enter_choose_region(self,event):
        title = '請先選擇一個城市'
        text = '我們有在您的城市提供送餐服務！'
        url = 'https://images.deliveryhero.io/image/foodpanda/hero-home-tw.jpg'
        btn = []
        if area == '北部':
            btn = [
                MessageTemplateAction(
                    label = '台北市',
                    text ='台北市'
                ),
                MessageTemplateAction(
                    label = '新北市',
                    text = '新北市'
                ),
                MessageTemplateAction(
                    label = '桃園市',
                    text ='桃園市'
                ),
                MessageTemplateAction(
                    label = '基隆市',
                    text ='基隆市'
                )
            ]
        elif area == '北中部':
            btn = [
                MessageTemplateAction(
                    label = '新竹市',
                    text ='新竹市'
                ),
                MessageTemplateAction(
                    label = '苗栗市',
                    text ='苗栗市'
                ),
                MessageTemplateAction(
                    label = '台中市',
                    text ='台中市'
                ),
                MessageTemplateAction(
                    label = '南投市',
                    text ='南投市'
                )
            ]
        elif area == '中南部':
            btn = [
                MessageTemplateAction(
                    label = '彰化市',
                    text ='彰化市'
                ),
                MessageTemplateAction(
                    label = '雲林縣',
                    text ='雲林縣'
                ),
                MessageTemplateAction(
                    label = '嘉義市',
                    text ='嘉義市'
                ),
                MessageTemplateAction(
                    label = '台南市',
                    text ='台南市'
                )
            ]
        elif area == '南部及外島':
            btn = [
                MessageTemplateAction(
                    label = '高雄市',
                    text ='高雄市'
                ),
                MessageTemplateAction(
                    label = '屏東縣',
                    text ='屏東縣'
                ),
                MessageTemplateAction(
                    label = '金門縣',
                    text ='金門縣'
                ),
                MessageTemplateAction(
                    label = '澎湖縣',
                    text ='彭湖縣'
                )
            ]  
        elif area == '東部':
            btn = [
                MessageTemplateAction(
                    label = '花蓮市',
                    text ='花蓮市'
                ),
                MessageTemplateAction(
                    label = '宜蘭縣',
                    text ='宜蘭縣'
                ),
                MessageTemplateAction(
                    label = '台東市',
                    text ='台東市'
                )
            ]
        
        send_button_message(event.reply_token, title, text, btn, url)  

    def is_going_to_choose_restaurant(self,event):
        global region
        text = event.message.text

        if text == '台北市':
            region = 'taipei'
            return True
        elif text == '新北市':
            region = 'new_taipei'
            return True
        elif text == '台中市':
            region = 'taichung'
            return True
        elif text == '高雄市':
            region = 'kaohsiung'
            return True
        elif text == '新竹市':
            region = 'hsinchu'
            return True
        elif text == '桃園市':
            region = 'taoyuan'
            return True
        elif text == '基隆市':
            region = 'keelung'
            return True
        elif text == '台南市':
            region = 'tainan'
            return True
        elif text == '苗栗市':
            region = 'miaoli'
            return True
        elif text == '嘉義市':
            region = 'chiayi'
            return True
        elif text == '彰化市':
            region = 'changhua'
            return True
        elif text == '宜蘭縣':
            region = 'yilan'
            return True
        elif text == '屏東縣':
            region = 'pingtung'
            return True
        elif text == '雲林縣':
            region = 'yunlin'
            return True
        elif text == '花蓮市':
            region = 'hualien'
            return True
        elif text == '南投市':
            region = 'nantou'
            return True
        elif text == '台東市':
            region = 'taitung'
            return True
        elif text == '澎湖縣':
            region = 'penghu'
            return True
        elif text == '金門縣':
            region = 'kinmen'
            return True
        
        return False

    def on_enter_choose_restaurant(self,event):
        title = '查看推薦的熱門餐廳'
        text = '選擇『推薦餐廳』或是『重新選擇城市』！'
        btn = [
            MessageTemplateAction(
                label = '推薦餐廳',
                text ='推薦餐廳'
            ),
            MessageTemplateAction(
                label = '重新選擇城市',
                text ='重新選擇城市'
            ),
        ]
        if(region == '台北市'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Tapei.jpg'
        elif(region == '新北市'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-New_Taipei.jpg'
        elif(region == '台中市'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Taichung.jpg'
        elif(region == '高雄市'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Kaohsiung.jpg'
        elif(region == '新竹市'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/City-tile-Hsinchu.jpg'
        elif(region == '桃園市'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/City-tile-taoyuan.jpg'
        elif(region == '基隆市'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Keelung.jpg'
        elif(region == '台南市'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Tainan.jpg'
        elif(region == '苗栗市'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-title-Miaoli.jpg'
        elif(region == '嘉義市'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-chiayi.jpg'
        elif(region == '彰化市'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-changhua.jpg'
        elif(region == '宜蘭縣'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Yilan.jpg'
        elif(region == '屏東縣'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Pingtung.jpg'
        elif(region == '雲林縣'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Yunlin.jpg'
        elif(region == '花蓮市'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Hualien.jpg'
        elif(region == '南投市'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Nantou.jpg'
        elif(region == '台東市'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Taitung.jpg'
        elif(region == '澎湖縣'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Penghu.jpg'
        elif(region == '金門縣'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Kinmen.jpg'

        send_button_message(event.reply_token, title, text, btn, url)    

    def is_going_to_recommand_restaurant(self,event):
        text = event.message.text

        if text == '推薦餐廳' or ((self.state == 'web_url' or self.state == 'recommand_menu') and text == "返回推薦餐廳"):
            return True
        
        return False

    def on_enter_recommand_restaurant(self,event):
        restaurant_list = pd.read_csv('./restaurant/' + region + '_info.csv')
        
        restaurant_id = random.randint(1,len(restaurant_list['id']))
        restaurant_info = restaurant_list[['name','link','pic_url','location','rating','count']][restaurant_id-1]
        restaurant_url = restaurant_info[1]

        title = restaurant_info[1] + '\n'+ '評價： ' + restaurant_info[4] + '/5 (' + restaurant_info[5] + ')\n' + '地址：' + restaurant_info[3]
        text = '選擇『餐廳網址』或是『推薦菜單』'
        btn = [
            MessageTemplateAction(
                label = '餐廳網址',
                text ='餐廳網址'
            ),
            MessageTemplateAction(
                label = '推薦菜單',
                text ='推薦菜單'
            ),
        ]
        url = restaurant_info[2]

        send_button_message(event.reply_token, title, text, btn, url)  
    
    def is_going_to_web_url(self,event):
        text = event.message.text

        if text == '餐廳網址':
            return True
        
        return False

    def on_enter_web_url(self,event):
        url = restaurant_url

        send_text_message(event.reply_token, url)

    def is_going_to_recommand_menu(self,event):
        text = event.message.text

        if text == '推薦菜單':
            return True
        
        return False

    def on_enter_recommand_menu(self,event):
        menu_list = pd.read_csv('./restaurant/' + region + '_menu.csv')
        menu = menu_list[menu_list['id'].str.contains(restaurant_id)]

        category = ''
        text = '以下為餐廳菜單：\n\n'
        for index,row in menu.iterrows():
            if row['category'] != category:
                category = row['category']
                text += row['category'] + '：\n'
            text += row['name'] + '\n\tNT$' + row['price'] + '\n'

        send_text_message(event.reply_token, text)


        


    




