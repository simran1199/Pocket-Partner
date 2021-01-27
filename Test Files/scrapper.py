import bs4 as bs
import sys
import time
import re
import urllib.request
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl


class Page(QWebEnginePage):

    def __init__(self, url):
        try:
            self.app = QApplication(sys.argv)
            print(15)
            QWebEnginePage.__init__(self)
            print(17)
            self.html = ''
            print(19)
            self.loadFinished.connect(self._on_load_finished)
            print(21)
            self.load(QUrl(url))
            print(23)
            self.app.exec_()
            print(25)
        except Exception as e:
            print(e)

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print(29)
        print('Load finished')
        print(31)

    def Callable(self, html_str):
        self.html = html_str
        print(35)
        self.app.quit()
        print(37)


def exact_url(url):
    index = url.find("B0")
    index = index + 10
    current_url = ""
    current_url = url[:index]
    return current_url


def get_converted_price(price):
    converted_price = float(re.sub(r"[^\d.]", "", price))
    return converted_price


def get_product_details(url):
    exacturl = exact_url(url)  # main url to extract data
    page = Page(exacturl)
    soup = bs.BeautifulSoup(page.html, 'html.parser')
    title = soup.find('span', id='productTitle')
    price = soup.find('span', id='priceblock_dealprice')
    details = {"name": "", "price": 0, "deal": True, "url": ""}

    if price is None:
        price = soup.find('span', id='priceblock_ourprice')
        details["deal"] = False

    if title is not None and price is not None:
        details["name"] = title.get_text().strip()
        details["price"] = get_converted_price(price.get_text())
        details["url"] = exacturl
        print("Both Not None")
    else:
        details = None
        print("Detail is None")
    return details


print(get_product_details("https://www.amazon.in/dp/B07HGJJ58K/"))
print(get_product_details("https://www.amazon.in/Test-Exclusive_2020_1113-Multi-3GB-Storage/dp/B089MS8XQ3/ref=gbph_tit_m-6_0518_97497036?smid=AQUYM0O99MFUT&pf_rd_p=fd83c15d-292e-4558-a082-4513fc550518&pf_rd_s=merchandised-search-6&pf_rd_t=101&pf_rd_i=1389401031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_r=F5X8AE2M7C17EMY5JYAX"))
