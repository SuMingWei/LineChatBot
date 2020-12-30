from transitions.extensions import GraphMachine

from utils import send_text_message,send_button_message,send_carousel_button_message

from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction,CarouselColumn
import pandas as pd
import numpy 
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
        send_carousel_button_message(event.reply_token)

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
        title = '我們有在您的城市提供送餐服務！'
        text = '選擇一個城市，或輸入『重新選擇地區』'
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
                    text ='澎湖縣'
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
        title = '查看'
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
        if(region == 'taipei'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Tapei.jpg'
            title += '台北市'
        elif(region == 'new_taipei'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-New_Taipei.jpg'
            title += '新北市'
        elif(region == 'taichung'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Taichung.jpg'
            title += '台中市'
        elif(region == 'kaohsiung'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Kaohsiung.jpg'
            title += '高雄市'
        elif(region == 'hsinchu'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/City-tile-Hsinchu.jpg'
            title += '新竹市'
        elif(region == 'taoyuan'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/City-tile-taoyuan.jpg'
            title += '桃園市'
        elif(region == 'keelung'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Keelung.jpg'
            title += '基隆市'
        elif(region == 'tainan'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Tainan.jpg'
            title += '台南市'
        elif(region == 'miaoli'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-title-Miaoli.jpg'
            title += '苗栗市'
        elif(region == 'chiayi'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-chiayi.jpg'
            title += '嘉義市'
        elif(region == 'changhua'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-changhua.jpg'
            title += '彰化市'
        elif(region == 'yilan'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Yilan.jpg'
            title += '宜蘭縣'
        elif(region == 'pingtung'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Pingtung.jpg'
            title += '屏東縣'
        elif(region == 'yunlin'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Yunlin.jpg'
            title += '雲林縣'
        elif(region == 'hualien'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Hualien.jpg'
            title += '花蓮市'
        elif(region == 'nantou'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Nantou.jpg'
            title += '南投市'
        elif(region == 'taitung'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Taitung.jpg'
            title += '台東市'
        elif(region == 'penghu'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Penghu.jpg'
            title += '澎湖縣'
        elif(region == 'kinmen'):
            url = 'https://images.deliveryhero.io/image/fd-tw/city-tile/city-tile-Kinmen.jpg'
            title += '金門縣'

        title += '的熱門餐廳'
        send_button_message(event.reply_token, title, text, btn, url)    

    def is_going_to_recommand_restaurant(self,event):
        text = event.message.text

        if text == '推薦餐廳' or ((self.state == 'recommand_menu' or self.state== 'recommand_restaurant') and text == "其他推薦餐廳"):
            return True
        
        return False

    def on_enter_recommand_restaurant(self,event):
        global restaurant_id,restaurant_url
        restaurant_list = pd.read_csv('./restaurant/' + region + '_info.csv')
        
        restaurant_id = random.randint(1,len(restaurant_list['id']))
        restaurant_info = restaurant_list[restaurant_id-1:restaurant_id]
        restaurant_url = restaurant_info['link'].values[0]

        title = restaurant_info['name'].values[0]
        text = '評價：' + str(restaurant_info['rating'].values[0]) + '/5 (' + str(restaurant_info['count'].values[0]) + ')\n' + '地址：' + restaurant_info['location'].values[0]
        btn = [
            URITemplateAction(
                label = '前往訂餐',
                uri = restaurant_url
            ),
            MessageTemplateAction(
                label = '快速瀏覽菜單',
                text ='快速瀏覽菜單'
            ),
            MessageTemplateAction(
                label = '其他推薦餐廳',
                text ='其他推薦餐廳'
            ),
        ]
        url = restaurant_info['pic_url'].values[0]

        send_button_message(event.reply_token, title, text, btn, url)  

    def is_going_to_recommand_menu(self,event):
        text = event.message.text

        if text == '快速瀏覽菜單':
            return True
        
        return False

    def on_enter_recommand_menu(self,event):
        menu_list = pd.read_csv('./restaurant/' + region + '_menu.csv')
        menu = menu_list[menu_list['id'].isin([restaurant_id])]

        category = ''
        text = '以下為餐廳菜單：\n\n'
        for index,row in menu.iterrows():
            if row['category'] != category:
                category = row['category']
                text += row['category'] + '：\n'
            text += row['name'] + '\n\tNT$' + str(row['price']) + '\n'

        send_text_message(event.reply_token, text)


        
    def is_going_to_web(self,event):
        text = event.message.text
        if(text.lower() == 'aneater'):
            return True

        return False

    def on_enter_web(self,event):
        title = '開始使用'
        text = '選擇『前往官網』或是『快速瀏覽』'
        btn = [
            URITemplateAction(
                label = '前往官網',
                uri = 'https://www.googleadservices.com/pagead/aclk?sa=L&ai=CaxDoNRTsX6XXOIWus8IPsMkBvqu281vF_6vT1gzRv-TpowEIABABILlUKAJgn5mhBqABo__WxAPIAQGpApIsYFdYnbQ-yAPYIKoEQE_QLZXbpvX5yk_PFgoU52hzmShj52Eo6e95p0mqD23OtZxR8IzRvBGLrOj3sUo2qump88C_8kbgOk1xm2KnApPABN7Q3Nj5AYAFkE6gBlGAB_zBizSIBwGQBwGoB6a-G6gH8NkbqAfy2RuoB_PRG6gH7tIbqAfK3BuwCAHSCAUQAiCEAZoJHWh0dHBzOi8vd3d3LmZvb2RwYW5kYS5jb20udHcvsQlrND7dw7-xgLkJazQ-3cO_sYD4CQGYCwGqDAIIAbgMAZgWAQ&ae=2&ved=2ahUKEwjAloq7gPXtAhWxIqYKHeO0DEAQ0Qx6BAgMEAE&dct=1&dblrd=1&sival=AF15MEASMV8VSt6rQ_Dl2o3-f0Hb0NvMydVMz3dLfibFcX8x9i-q7kFoHNawtvHzciAzq-X0ESp0WGjFIfVcjnVoNK4NKDiqVrD4jd6BjMDEGn5ILP2KzhODk6A0F99fSM20fPxOpK5Z-YI1kcj-rSNmiqMX7IVlDg&sig=AOD64_1oYAeLPfa51FceuW0wzqW4zK8LiQ&adurl=https://www.foodpanda.com.tw/'
            ),
            MessageTemplateAction(
                label = '快速瀏覽',
                text ='快速瀏覽'
            ),
        ]
        url = 'https://assets.foodora.com/f6f5bef/img/favicon/foodpanda/apple-touch-icon-57x57.png?f6f5bef'

        send_button_message(event.reply_token, title, text, btn, url)          

    




