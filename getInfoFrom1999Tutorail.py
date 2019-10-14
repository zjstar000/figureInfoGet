import requests
import pymongo
import re
import datetime
from pyquery import PyQuery as pq

url = 'https://www.1999.co.jp/search?typ1_c=101&cat=&state=&sold=0&sortid=0&searchkey=%e8%81%96%e9%97%98%e5%a3%ab'
headers = {
    'User-Agent': 'Mozilla/5.0(Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36(KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}


# @param: gene items' generator
# @return: generrator next twice
# called by function getPrice
def nextTwice(gene):
    gene.__next__()
    return gene.__next__()


# @param: gene items' generator
# @return: price(int) of this item
def getPrice(gene):
    price = 0
    priceStr = nextTwice(gene).text()
    patternPrice = re.compile(r'[\d,]+[\d]')
    m = patternPrice.findall(priceStr)
    print(m)
    if len(m) > 0:
        price = m[-1]
        if ',' in price:
            price = price.replace(",", "")
            print(price)
    return int(price)


# @param: str
# @return: パラメタのstrにある全ての数字が組み合わせる後のint
def getIntFromStr(str):
    patternNum = re.compile(r"\d")
    resNum = patternNum.findall(str)
    numStr = ""
    for num in resNum:
        numStr = numStr + num
    return int(numStr)


def getTime(str):
    print(str)
    patternYyyy = re.compile(r"(\d{1,4}年|\d{4}\/)")
    patternMm = re.compile(r"(\d{1,2}月|\/\d{1,2}\/)")
    patternDd = re.compile(r"(\d{1,2}日|\/\d{1,2}[^\/])")

    resYear = patternYyyy.search(str)
    if not resYear:
        year = 9999
    else:
        year = getIntFromStr(resYear.group(0))

    resMonth = patternMm.search(str)
    if not resMonth:
        month = 1
    else:
        month = getIntFromStr(resMonth.group(0))

    resDay = patternDd.search(str)
    if not resDay:
        day = 1
    else:
        day = getIntFromStr(resDay.group(0))
    return datetime.datetime(year, month, day)


# Main Logic
html = requests.get(url, headers=headers).text
doc = pq(html)

# item sections
sections = doc('#masterBody_pnlSearch').find('div[id = "divListRow"]').items()
print(doc('#masterBody_pnlSearch').find('div[id = "divListRow"]').size())

# DB接続
client = pymongo.MongoClient(host='localhost', port=27017)
db = client.item
collection = db.item

# 既存データ削除
collection.delete_many({})

i = 0

for section in sections:
    # if i > 0:
    #     break
    itemInfos = section.children().items()
    print(section.children().size())
    for iteminfo in itemInfos:
        i = i + 1
        itemName = iteminfo.find('[id*="lblItemName"]').text()
        itemDetails = iteminfo.find('[id*="lblVal"]').items()
        collection.insert_one({
            "name": itemName,
            "maker": itemDetails.__next__().text(),
            "time": getTime(itemDetails.__next__().text()),
            "price": getPrice(itemDetails),
            "category": itemDetails.__next__().text(),
        })

