import requests
from bs4 import BeautifulSoup
import smtplib

URL = "https://www.amazon.in/Fujifilm-Instax-Mini-Instant-Camera/dp/B08527W1MF/ref=sr_1_1_sspa?dchild=1&keywords=instax+mini&qid=1611431864&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExTThVWEkyNzE0UkpCJmVuY3J5cHRlZElkPUEwMDc3NjEwM0JHREdYVEdQRkJEVyZlbmNyeXB0ZWRBZElkPUEwMDg5NzMzMzVZRlJYVFlOVUk0JndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=="

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}


def chckprice():
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text()
    converted_price = float(price[2:3])

    if(converted_price < 6):
        send_mail()

    print(converted_price)
    print(title.strip())


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


chckprice()
