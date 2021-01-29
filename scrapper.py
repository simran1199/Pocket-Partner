import requests
from bs4 import BeautifulSoup
import smtplib
import re
import json

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}


# to extract only the necessary part of the product's url
def extract_url(url):
    index = url.find("B0")
    index = index + 10
    current_url = ""
    current_url = url[:index]
    print(current_url)
    return current_url


# function to scrap product details
def get_product_details(url):
    url = extract_url(url)
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    # product's name
    title = soup.find(id="productTitle").get_text().strip()
    # product's price
    price = soup.find(id="priceblock_dealprice")
    print(price)
    if price == None:
        price = soup.find(id="priceblock_ourprice")
        print(price)
    if price == None:
        price = soup.find(id="priceblock_salesprice")
    # product's availability
    availability = soup.find(id="availability").get_text().strip()
    # product's image
    img_div = soup.find(id="imgTagWrapperId")
    # a string in Json format
    imgs_str = img_div.img.get('data-a-dynamic-image')
    # convert to a dictionary
    imgs_dict = json.loads(imgs_str)
    # each key in the dictionary is a link of an image, and the value shows the size (print all the dictionay to inspect)
    num_element = 0
    first_link = list(imgs_dict.keys())[num_element]
    image = first_link

    converted_price = float(re.sub(r"[^\d.]", "", price.get_text()))

    details = {"name": title, "price": converted_price, "url": url,
               "availability": availability, "image_url": image}
    return details


# for sending emails
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
