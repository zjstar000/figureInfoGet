import random
import requests
import os
from itemDetail import ItemDetail
from urlHeaders import UrlHeaders
from image import Image
from pyquery import PyQuery as pq

base_url = "https://www.1999.co.jp/"
matchFlg = False

missTimes = 0
for num in range(10311000, 10312000):

    # debug start
    # if matchFlg:
    #     break
    # debug end

    # num = random.randint(10300000, 10700000)
    url = base_url + str(num)

    # get info
    res = requests.get(url, headers=UrlHeaders.getHeader())
    if res.status_code == 200:
        html = res.text
        print("url = {}".format(url))
        item = ItemDetail(html)
        # 商品コードがないitemをとりあえず無視する
        if ("フィギュア" not in item.getCategory() and "ロボット" not in item.getCategory()) or item.getShohinCd() is None or item.getJanCode() is None:
            continue
        # get img
        img_saved_path = ""
        # フィギュアのみ
        # 商品の画像一覧サイト
        img_base_url = "https://www.1999.co.jp/image/"
        img_url = img_base_url + str(num)
        img_res = requests.get(img_url, headers=UrlHeaders.getHeader())
        if img_res.status_code == 200:
            img_html = img_res.text
            img_doc = pq(img_html)
            img_items = img_doc('#imgAll > div > img').items()
            img_item_path = "imgFrom1999/"
            index = 0
            for img_item in img_items:
                index += 1
                # 画像ファイルのurl
                img_item_url = base_url + img_item.attr('src')
                # 画像保存する場所
                img_item_path = "imgFrom1999/"
                img_name = item.getShohinCd() + "_" + str(index)
                image = Image(img_item_url, img_item_path, img_name)
                image.saveImg()
            saved_path = os.path.dirname(__file__).join(img_item_path)

        item.preserving(img_saved_path)

        # debug用
        matchFlg = True

    else:
        missTimes += 1
        continue

print("missTimes = {}".format(missTimes))
