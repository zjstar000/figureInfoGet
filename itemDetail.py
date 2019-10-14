import requests
import re
from urlHeaders import UrlHeaders

from pyquery import PyQuery as pq


class ItemDetail(object):
    __itemOtherDict = {}

    def __init__(self, url, headers=UrlHeaders.getHeader()):
        self.url = url
        print(self.url)
        self.headers = headers
        self.__getPqDoc()
        self.__setOtherInfo()

    def __getPqDoc(self):
        html = requests.get(self.url, headers=self.headers).text
        with open("html.txt", "w") as file:
            file.write(html)
        self.doc = pq(html)

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

    # 発売予定日
    def getSalesDate(self):
        tr = self.doc('#masterBody_trSalesDate').items().__next__()
        return tr.find('td:last-child').text()

    # 参考価格
    def getStickerPrice(self):
        tr = self.doc('#masterBody_trStickerPrice').items().__next__()
        return tr.find('td:last-child').text()

    # 1999価格
    def get1999Price(self):
        tr = self.doc('#masterBody_trPrice').items().__next__()
        return tr.find('td:last-child').text()

    # JANコード
    def getJanCode(self):
        tr = self.doc('#masterBody_trJanCode').items().__next__()
        return tr.find('td:last-child').text()

    # 商品コード
    def getShohinCd(self):
        return self.__itemOtherDict.get("商品コード")

    # 情報をDBに反映
    def preserving(self):
        # TODO 未実装
        return


url = "https://www.1999.co.jp/10647856"
item = ItemDetail(url)

print("ItemName: {}".format(item.getItemName()))
print("Ranking?: {}".format(item.getRanking()))
print("R18?: {}".format(item.getIsAdult()))
print("New?: {}".format(item.getIsNew()))
print("marker = {}".format(item.getMaker()))
print("scale = {}".format(item.getScale()))
print("material = {}".format(item.getMaterial()))
print("serise = {}".format(item.getSeries()))
print("author = {}".format(item.getAuthor()))
print("from = {}".format(item.getFrom()))
print("salesDate = {}".format(item.getSalesDate()))
print("stickerPrice = {}".format(item.getStickerPrice()))
print("1999Price = {}".format(item.get1999Price()))
print("JANcode = {}".format(item.getJanCode()))
print("shohinCd = {}".format(item.getShohinCd()))