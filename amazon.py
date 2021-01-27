from selectorlib import Extractor
import requests
import json
import re
from time import sleep
import sqlite3


# Creating an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('selectors.yml')


def get_converted_price(price):
    converted_price = float(re.sub(r"[^\d.]", "", price))
    return converted_price


def extract_url(url):
    index = url.find("B0")
    index = index + 10
    current_url = ""
    current_url = url[:index]
    print(current_url)
    return current_url


def scrape(url):
    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s" % url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print(
                "Page %s was blocked by Amazon. Please try using better proxies\n" % url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d" % (
                url, r.status_code))
        return None
<<<<<<< HEAD
    # Pass the HTML of the page and create 
    text_file = open("sample.txt", "w")
    n = text_file.write(r.text)
    text_file.close()
=======
    # Pass the HTML of the page and create
>>>>>>> ee0a4fe3f36393ba6cf218faf1471e3943e954a1
    return e.extract(r.text)


def get_product_details(url):
    url = extract_url(url)

    data = scrape(url)
    if data:
        data['url'] = url
        if data['price']:
            data['price'] = get_converted_price(data['price'])
        if data['resprice']:
            data['resprice'] = get_converted_price(data['resprice'])
        return data
<<<<<<< HEAD
    
print(get_product_details("https://www.amazon.in/Test-Exclusive_2020_1113-Multi-3GB-Storage/dp/B089MS8XQ3/ref=gbph_tit_m-6_0518_97497036?smid=AQUYM0O99MFUT&pf_rd_p=fd83c15d-292e-4558-a082-4513fc550518&pf_rd_s=merchandised-search-6&pf_rd_t=101&pf_rd_i=1389401031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_r=F5X8AE2M7C17EMY5JYAX"))
=======

# print(get_product_details("https://www.amazon.in/Test-Exclusive_2020_1113-Multi-3GB-Storage/dp/B089MS8XQ3/ref=gbph_tit_m-6_0518_97497036?smid=AQUYM0O99MFUT&pf_rd_p=fd83c15d-292e-4558-a082-4513fc550518&pf_rd_s=merchandised-search-6&pf_rd_t=101&pf_rd_i=1389401031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_r=F5X8AE2M7C17EMY5JYAX"))
>>>>>>> ee0a4fe3f36393ba6cf218faf1471e3943e954a1
# print(get_product_details("https://www.amazon.in/dp/B07HGJJ58K/"))
# print(get_product_details("https://www.amazon.in/Test-Exclusive_2020_1113-Multi-3GB-Storage/dp/B089MS8XQ3/ref=gbph_tit_m-6_0518_97497036?smid=AQUYM0O99MFUT&pf_rd_p=fd83c15d-292e-4558-a082-4513fc550518&pf_rd_s=merchandised-search-6&pf_rd_t=101&pf_rd_i=1389401031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_r=F5X8AE2M7C17EMY5JYAX"))
