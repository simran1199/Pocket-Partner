import requests
import re
from bs4 import BeautifulSoup
from itertools import cycle
import traceback
from lxml.html import fromstring

def get_converted_price(price):
    
    # stripped_price = price.strip("₹ ,")
    # replaced_price = stripped_price.replace(",", "")
    # find_dot = replaced_price.find(".")
    # to_convert_price = replaced_price[0:find_dot]
    # converted_price = int(to_convert_price)
    converted_price = float(re.sub(r"[^\d.]", "", price))
    return converted_price


def extract_url(url):

    # if url.find("www.amazon.in") != -1:
    #     index = url.find("/dp/")
    #     if index != -1:
    #         index2 = index + 14
    #         url = "https://www.amazon.in" + url[index:index2]
    #     else:
    #         index = url.find("/gp/")
    #         if index != -1:
    #             index2 = index + 22
    #             url = "https://www.amazon.in" + url[index:index2]
    #         else:
    #             url = None
    # else:
    #     url = None
    # print(url)
    # return url
    index = url.find("B0") 
    index = index + 10
    current_url = "" 
    current_url = url[:index] 
    print(current_url)
    return current_url 

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


def get_product_details(url):

    headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    proxies = {
            'http': 'http://203.115.112.218:3128',
            'https': 'http://203.115.112.218:3128',
            }

    details = {"name": "", "price": 0, "deal": True, "url": ""}
    _url = extract_url(url)
    # _url = url
    if _url is None:
        details = None
        print("URL is None")
    else:
        proxies = get_proxies()
        proxy_pool = cycle(proxies)
        for i in range(1,11):
        #Get a proxy from the pool
            proxy = next(proxy_pool)
            print("Request #%d"%i)
            try:
                page = requests.get(url,proxies={"http": proxy, "https": proxy})
                print(page.json())
            except:
                #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work. 
                #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url 
                print("Skipping. Connnection error")
                
                
        # page = requests.get(_url,proxies=proxies)
        soup = BeautifulSoup(page.content, "html5lib")
        
        # soup = BeautifulSoup(page.content, 'html.parser') 
        print(soup)
        title = soup.find(id='productTitle')
        price = soup.find(id ='priceblock_dealprice') 
        print(price)
        print(title)
        if price is None:
            price = soup.find(id='priceblock_ourprice')
            details["deal"] = False
            print("Price is None")
        if title is not None and price is not None:
            details["name"] = title.get_text().strip()
            details["price"] = get_converted_price(price.get_text())
            details["url"] = _url
            print("Both Not None")
        else:
            details = None
            print("Detail is None")
    return details


print(get_product_details("https://www.amazon.in/Test-Exclusive_2020_1113-Multi-3GB-Storage/dp/B089MS8XQ3/ref=gbph_tit_m-6_0518_97497036?smid=AQUYM0O99MFUT&pf_rd_p=fd83c15d-292e-4558-a082-4513fc550518&pf_rd_s=merchandised-search-6&pf_rd_t=101&pf_rd_i=1389401031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_r=F5X8AE2M7C17EMY5JYAX"))
