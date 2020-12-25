import requests
from bs4 import BeautifulSoup,element
import pandas as pd
from re import search
import time

HOME_URL = "https://www.foodpanda.com.tw"

# 取得所有城市的連結
def get_all_city_link():  
    response = requests.get(HOME_URL)
    soup = BeautifulSoup(response.text,"html.parser")
    all_a = soup.find_all("a",class_="city-tile")
    all_link = [HOME_URL+a.get("href") for a in all_a ]

    return all_link

# 取得餐廳資訊
def get_restaurant_info(url):  
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")   
    all_li = soup.find("ul",class_="vendor-list").children

    all_restaurant = []
    for v in all_li:
        if isinstance(v,element.Tag):
            all_restaurant.append(v)
            
    restaurants_info = []
    for restaurant in all_restaurant:
        v = {}
        #restaurant name
        v["name"] = restaurant.find("span",class_="name fn").text
        #restaurant link
        v["link"] = HOME_URL+restaurant.find("a").get('href')
        #restaurant photo
        pic_url = restaurant.find("div").get("data-src")
        v["pic_url"] = pic_url[:pic_url.find("?")]
        #restaurant location
        response2 = requests.get(v["link"])
        soup2 = BeautifulSoup(response2.text,"html.parser")
        v["location"] = soup2.find("div",class_="content").find("p",class_="vendor-location").text
        #restaurant star
        try:
            v["rating"] = restaurant.find("span",class_="rating").find("strong").text
            v["count"] = restaurant.find("span",class_="count").text.strip()
        except:
            v["rating"] = "NA"
            v["count"] = 0
            
        restaurants_info.append(v)
    return pd.DataFrame(restaurants_info)

# 取得菜單
def get_restaurant_menu(url):
    menu = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")
    dishes_section = soup.find_all("div",class_="dish-category-section")
    for section in dishes_section:
        #restaurant menu-category
        category = section.find("h2",class_="dish-category-title").text
        dishes = section.find("ul",class_="dish-list").find_all("li")
        for dish in dishes:
            m = {}
            m["category"] = category
            #dish name
            m["name"] = dish.find("h3").find("span").text
            #dis price
            m["price"] = dish.find("span",class_="price p-price").text.strip()
            menu.append(m)
    return menu

def extract_number(str_num):
    pattern = "[\d,]+.[\d]{2}"
    return search(pattern, str_num).group(0)

def get_all_info(num,name):
    cities_link = get_all_city_link()

    restaurants_info = get_restaurant_info(cities_link[num])
    restaurants_info.insert(0,"id",[i for i in range(1,len(restaurants_info)+1)])

    menu_list = []
    for id_, link in zip(restaurants_info["id"].values,restaurants_info["link"].values):
        menu = get_restaurant_menu(link)
        #add restaurant ID
        for i in range(len(menu)):
            menu[i]["id"] = id_
        menu_list.extend(menu)
        
    restaurants_menu = pd.DataFrame(menu_list)

    restaurants_menu.price = restaurants_menu.price.apply(extract_number)
    restaurants_menu.price = restaurants_menu.price.apply(lambda price:price.replace(",",""))

    #remove unnessary category
    unwanted_category = ["注意事項","營養標示"]
    unwanted_index = []
    for category in unwanted_category:
        index = restaurants_menu[restaurants_menu.category.str.contains(category)].index
        if len(index)>1:
            unwanted_index.extend(index)
    restaurants_menu.drop(unwanted_index, axis=0,inplace=True)

    restaurants_info.count = restaurants_info["count"].astype(int)
    restaurants_menu.price = restaurants_menu["price"].astype(float)

    # output csv
    path1 = "./restaurant/" + name + "_info.csv"
    path2 = "./restaurant/" + name + "_menu.csv"
    restaurants_info.to_csv(path1,index=False)
    restaurants_menu.to_csv(path2,index=False)


if __name__ == "__main__":

    # get_all_info(0,'taipei')
    # get_all_info(1,'new_taipei')
    # get_all_info(2,'taichung')
    # get_all_info(3,'kaohsiung')
    # get_all_info(4,'hsinchu')
    # get_all_info(5,'taoyuan')
    # get_all_info(6,'keelung')
    # get_all_info(7,'tainan')
    # get_all_info(8,'miaoli')
    # get_all_info(9,'chiayi')
    # get_all_info(10,'changhua')
    # get_all_info(11,'yilan')
    # get_all_info(12,'pingtung')
    # get_all_info(13,'yunlin')
    # get_all_info(14,'hualien')
    # get_all_info(15,'nantou')
    # get_all_info(16,'taitung')
    # get_all_info(17,'penghu')
    get_all_info(18,'kinmen')

