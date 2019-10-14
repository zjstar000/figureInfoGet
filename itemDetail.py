import requests
import re
from urlHeaders import UrlHeaders

from pyquery import PyQuery as pq


class ItemDetail(object):
    __itemInfoDict = {}

    def __init__(self, url, headers=UrlHeaders.getHeader()):
        self.url = url
        print(self.url)
        self.headers = headers
        self.__getPqDoc()
        self.__setItemInfo()

    def __getPqDoc(self):
        html = requests.get(self.url, headers=self.headers).text
        with open("html.txt", "w") as file:
            file.write(html)
        self.doc = pq(html)

    def __setOtherInfo(self):
        key = []
        value = []
        tbodyItems = self.doc('#tblItemInfo').items()
        for tbodyItem in tbodyItems:
            trs = tbodyItem.find('tr').items()
            # メーカー
            mkTds = trs.__next__().find('td').items()
            mkTitleTd = mkTds.__next__()
            mkHrefTd = mkTds.__next__()
            mkContent = mkTds.__next__().text()
            key.append("maker")
            value.append(mkContent)

            # スケール
            scTds = trs.__next__().find('td').items()
            scTitleTd = scTds.__next__()
            scHrefTd = scTds.__next__()
            scContent = scTds.__next__().text()
            key.append("scale")
            value.append(scContent)

            # 素材
            szTds = trs.__next__().find('td').items()
            szTitleTd = szTds.__next__()
            szHrefTd = szTds.__next__()
            szContent = szTds.__next__().text()
            key.append("material")
            value.append(szContent)

            # 原型制作
            gkTds = trs.__next__().find('td').items()
            gkTitleTd = gkTds.__next__()
            gkHrefTd = gkTds.__next__()
            gkContent = gkTds.__next__().text()
            key.append("author")
            value.append(gkContent)

            # 原作
            gsTds = trs.__next__().find('td').items()
            gsTitleTd = gsTds.__next__()
            gsHrefTd = gsTds.__next__()
            gsContent = gsTds.__next__().text()
            key.append("from")
            value.append(gsContent)

            # 発売予定日

            # 参考価格

            # 代引前払価格

            # 通常価格

            # 取得ポイント

            # JANコード

            # 商品コード

            self.__itemInfoDict = dict(zip(key, value))

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
        return self.itemInfoDict.get("maker")

    # スケール

    # 素材

    # 原型制作

    # 原作

    # 発売予定日

    # 参考価格

    # 代引前払価格

    # 通常価格

    # 取得ポイント

    # JANコード

    # 商品コード


url = "https://www.1999.co.jp/10647918"
item = ItemDetail(url)

print("ItemName: {}".format(item.getItemName()))
print("Ranking?: {}".format(item.getRanking()))
print("R18?: {}".format(item.getIsAdult()))
print("New?: {}".format(item.getIsNew()))
print("marker = {}".format(item.getMaker()))
