import re
import pymongo
import datetime
from urlHeaders import UrlHeaders
import requests

from pyquery import PyQuery as pq


class ItemDetail(object):
    __itemOtherDict = {}
    __base_url = "https://www.1999.co.jp/"

    def __init__(self, html):
        self.html = html
        self.__getPqDoc()
        self.__setOtherInfo()

    def __getPqDoc(self):
        with open("html.txt", "w") as file:
            file.write(self.html)
        self.doc = pq(self.html)

    # 発売日及び値段、ポイント（取得しない）JANコード以外の情報をitemOtherDictに保存しとく
    def __setOtherInfo(self):
        key = []
        value = []
        tbodyItem = self.doc('#tblItemInfo').items().__next__()
        trs = tbodyItem.find('tr:not([id^="masterBody_"])').items()
        for tr in trs:
            if tr.find('td').size() == 3:
                tds = tr.find('td').items()
                titleTd = tds.__next__().text()
                # とりあえず取るだけで使っていない
                hrefTd = tds.__next__()
                contentTd = tds.__next__().text()
                key.append(str.strip(titleTd))
                value.append(str.strip(contentTd))
            else:
                continue
        self.__itemOtherDict = dict(zip(key, value))

    # @param: str
    # @return: パラメタのstrにある全ての数字が組み合わせる後のint
    @staticmethod
    def __getIntFromStr(str):
        patternNum = re.compile(r"\d")
        resNum = patternNum.findall(str)
        numStr = ""
        for num in resNum:
            numStr = numStr + num
        return int(numStr)

    # @param: str
    # @return: パラメタのstrから日付の情報を洗いだし、datetimeタイプとして戻す
    def __getDate(self, str):
        patternYyyy = re.compile(r"(\d{1,4}年|\d{4}\/)")
        patternMm = re.compile(r"(\d{1,2}月|\/\d{1,2}\/)")
        patternDd = re.compile(r"(\d{1,2}日|/\d{1,2}[^/\d])")

        resYear = patternYyyy.search(str)
        if not resYear:
            year = 9999
        else:
            year = self.__getIntFromStr(resYear.group(0))

        resMonth = patternMm.search(str)
        if not resMonth:
            month = 1
        else:
            month = self.__getIntFromStr(resMonth.group(0))

        resDay = patternDd.search(str)
        if not resDay:
            day = 1
        else:
            day = self.__getIntFromStr(resDay.group(0))
        return datetime.datetime(year, month, day)

    # @param: gene items' generator
    # @return: price(int) of this item
    @staticmethod
    def __getPrice(priceStr):
        price = 0
        patternPrice = re.compile(r'[\d,]+[\d]')
        m = patternPrice.findall(priceStr)
        if len(m) > 0:
            price = m[-1]
            if ',' in price:
                price = price.replace(",", "")
        return int(price)

    # Item名称
    def getItemName(self):
        return self.doc('.h2_itemDetail').text()

    # R18であるか
    def getIsAdult(self):
        return self.doc('img[id^="masterBody_"][title^="18"]').size() > 0

    # 新品であるか
    def getIsNew(self):
        return self.doc('img[id^="masterBody_"][title^="新"]').size() > 0

    # ランキング入りであるか
    def getRanking(self):
        ranking = 0
        rankResult = self.doc('#masterBody_tblItemImg').find('img[title*="位"]')
        if rankResult.size() > 0:
            rankTitle = rankResult.items().__next__().attr("title")
            pattern = re.compile(r"\d*位")
            reRes = pattern.search(rankTitle)
            if reRes:
                ranking = re.search(r"\d*", reRes.group(0)).group(0)
        return ranking

    # メーカー
    def getMaker(self):
        return self.__itemOtherDict.get("メーカー")

    # スケール
    def getScale(self):
        return self.__itemOtherDict.get("スケール")

    # 素材
    def getMaterial(self):
        return self.__itemOtherDict.get("素材")

    # シリーズ
    def getSeries(self):
        return self.__itemOtherDict.get("シリーズ")

    # 原型制作
    def getAuthor(self):
        return self.__itemOtherDict.get("原型制作")

    # 原作
    def getFrom(self):
        return self.__itemOtherDict.get("原作")

    # 発売日
    def getSalesDate(self):
        salesDate = None
        self.dateStr = ""
        if self.doc('#masterBody_trSalesDate').size() > 0:
            tr = self.doc('#masterBody_trSalesDate').items().__next__()
            self.dateStr = tr.find('td:last-child').text()
            if self.dateStr:
                salesDate = self.__getDate(self.dateStr)
        return salesDate

    # 予定日
    def getYoteiDate(self):
        yykDate = None
        if self.dateStr and "予約" in self.dateStr:
            parttern = re.compile(r"(\d+|\d+/+\d+|\d+/\d+/\d+)予約")
            yykDateStr = parttern.search(self.dateStr).group(0)
            yykDate = self.__getDate(yykDateStr)
        return yykDate

    # 参考価格
    def getStickerPrice(self):
        stickerPrice = None
        if self.doc('#masterBody_trStickerPrice').size() > 0:
            tr = self.doc('#masterBody_trStickerPrice').items().__next__()
            stickerPrice = tr.find('td:last-child').text()
        return stickerPrice

    # 1999価格
    def get1999Price(self):
        e1999Price = None
        if self.doc('#masterBody_trPrice').size() > 0:
            tr = self.doc('#masterBody_trPrice').items().__next__()
            e1999Price = tr.find('td:last-child').text()
        return e1999Price

    # JANコード
    def getJanCode(self):
        janCode = None
        if self.doc('#masterBody_trJanCode').size() > 0:
            tr = self.doc('#masterBody_trJanCode').items().__next__()
            janCode = tr.find('td:last-child').text()
        return janCode

    # 商品コード
    def getShohinCd(self):
        return self.__itemOtherDict.get("商品コード")

    # カテゴリ
    def getCategory(self):
        category = None
        if self.doc('.item_genre').find('a').size() > 0:
            item = self.doc('.item_genre').find('a').items().__next__()
            category = item.attr("title")
        return category


    # 情報をDBに反映
    def preserving(self, imgPath=""):
        client = pymongo.MongoClient(host='localhost', port=27017)
        db = client.item
        collection = db.item
        # # 既存データ削除
        # collection.delete_many({})
        currentItem = {
            'janCd': self.getJanCode(),
            'itemName': self.getItemName(),
            'ranking': self.getRanking(),
            'r18': self.getIsAdult(),
            'new': self.getIsNew(),
            'marker': self.getMaker(),
            'from': self.getFrom(),
            'salesDate': self.getSalesDate(),
            'yykDate': self.getYoteiDate(),
            'stickerPrice': self.__getPrice(self.getStickerPrice()),
            '1999Price': self.__getPrice(self.get1999Price()),
            'shohinCd': self.getShohinCd(),
            'imagePath': imgPath,
            'category': self.getCategory(),
        }

        # データはすでに保存したかをチェックする
        condition = {"shohinCd": self.getShohinCd()}
        findResult = collection.find_one(condition)
        if findResult:
            changedFlg = collection.find_one(currentItem)
            if not changedFlg:
                currentItem['updatedDate'] = datetime.datetime.now()
            collection.update_one(condition, {'$set': currentItem})
        else:
            currentItem['insertedDate'] = datetime.datetime.now()
            collection.insert_one(currentItem)

# for debugging
# url = "https://www.1999.co.jp/10630979"
# item = ItemDetail(url)
# item.preserving()
# for debugging
# print("ItemName: {}".format(item.getItemName()))
# print("Ranking?: {}".format(item.getRanking()))
# print("R18?: {}".format(item.getIsAdult()))
# print("New?: {}".format(item.getIsNew()))
# print("marker = {}".format(item.getMaker()))
# print("scale = {}".format(item.getScale()))
# print("material = {}".format(item.getMaterial()))
# print("serise = {}".format(item.getSeries()))
# print("author = {}".format(item.getAuthor()))
# print("from = {}".format(item.getFrom()))
# print("salesDate = {}".format(item.getSalesDate()))
# print("yykDate = {}".format(item.getYoteiDate()))
# print("stickerPrice = {}".format(item.getStickerPrice()))
# print("1999Price = {}".format(item.get1999Price()))
# print("JANcode = {}".format(item.getJanCode()))
# print("shohinCd = {}".format(item.getShohinCd()))
# print("shohinCd = {}".format(item.getCategory()))
