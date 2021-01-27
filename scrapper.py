import requests
from bs4 import BeautifulSoup
import smtplib
import re

#URL = "https://www.amazon.in/Amazon-Brand-Microfibre-Reversible-Comforter/dp/B01LTI1KFU"
#URL = "https://www.amazon.in/Panasonic-Semi-Automatic-Loading-NA-W70E5RRB-Powerful/dp/B08B97BVJF/ref=sr_1_1_sspa?dchild=1&pf_rd_p=05edb6d2-4c62-4d07-9331-f6ee94c74e5b&pf_rd_r=NQKBB2PDH8Z4HFX2RWRV&qid=1611759986&refinements=p_85%3A10440599031&rps=1&s=kitchen&sr=1-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyNEZaME5XQ0wwSFFXJmVuY3J5cHRlZElkPUEwNzk1MTEwMjlBV09aNkpXQUlBVyZlbmNyeXB0ZWRBZElkPUEwMDIyNTU5N0NKM1VUVTJUVTk3JndpZGdldE5hbWU9c3BfYXRmX2Jyb3dzZSZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU="

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}


def extract_url(url):
    index = url.find("B0")
    index = index + 10
    current_url = ""
    current_url = url[:index]
    print(current_url)
    return current_url


def get_product_details(url):
    url = extract_url(url)
    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle").get_text().strip()
    price = soup.find(id="priceblock_dealprice")
    if price == None:
        price = soup.find(id="priceblock_ourprice")
    if price == None:
        price = soup.find(id="priceblock_salesprice")

    converted_price = float(re.sub(r"[^\d.]", "", price.get_text()))

    details = {"name": title, "price": converted_price, "url": url}
    return details


def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    # here i have used my email with temporary password for senders email
    server.login('simran3579singh@gmail.com', 'irokaeeswojzasfu')

    subject = 'the price fell down'
    body = 'check the amazon link => https://www.amazon.in/Fujifilm-Instax-Mini-Instant-Camera/dp/B08527W1MF/ref=sr_1_1_sspa?dchild=1&keywords=instax+mini&qid=1611431864&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExTThVWEkyNzE0UkpCJmVuY3J5cHRlZElkPUEwMDc3NjEwM0JHREdYVEdQRkJEVyZlbmNyeXB0ZWRBZElkPUEwMDg5NzMzMzVZRlJYVFlOVUk0JndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=='
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        'simran3579singh@gmail.com',
        # (recievers email) use your email here for recieving emails.
        '184085@nith.ac.in',
        msg
    )
    print('email sent')
    server.quit()
