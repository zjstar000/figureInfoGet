import requests
import os
from urlHeaders import UrlHeaders


# param
# url: 画像ファイルのurl
# dirc: 保存するパス
# img_name: 設定する画像名
class Image(object):

    def __init__(self, url, dirc, img_name):
        self.url = url
        self.dirc = dirc
        self.img_name = img_name
        res = requests.get(url, headers=UrlHeaders.getHeader())
        if res.status_code != 200:
            self.img_content = None
            return
        else:
            self.img_content = res.content

    # 保存時のファイル名を生成する
    def _setFilename(self):
        original_filename = self.url.split("/")[-1]
        extension = original_filename.split(".")[-1]
        filename = self.img_name + "." + extension
        return filename

    def saveImg(self):
        filename = self._setFilename()
        filepath = self.dirc + filename
        with open(filepath, 'wb') as file:
            file.write(self.img_content)
