import random
import requests
import itemDetail
from itemDetail import ItemDetail
from urlHeaders import UrlHeaders

base_url = "https://www.1999.co.jp/"

missTimes = 0
for i in range(100):
    num = random.randint(10000000, 20000000)
    url = base_url + str(num)
    res = requests.get(url, headers=UrlHeaders.getHeader())
    if res.status_code == 200:
        html = res.text
        print("url = {}".format(url))
        item = ItemDetail(html)
        item.preserving()
    else:
        missTimes += 1
        continue

print("missTimes = {}".format(missTimes))
