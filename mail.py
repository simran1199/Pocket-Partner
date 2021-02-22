import requests
import smtplib


def send_mail(frmTable, frmScrapper):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    email = 'pcktpartner@gmail.com'
    password = 'pocketpartner@4'
    server.login(email, password)

    subject = "Yay, The Price Dropped!!"
    body1 = f"Hey {frmTable['name']}, \n\n"
    body2 = f"The Price of the following product dropped: \n\n \t\t{frmTable['product']} \n \t\tOld Price: Rs. {frmScrapper['price']} \n \t\tCurrent Price: Rs. {frmTable['price']}\n\n"
    body3 = f"Head to the below URL and complete your purchase now: {frmTable['url']}\n\n"
    body4 = "Once ordered, do remember to delete the product from your profile to stop further notifications.\n\n"
    body5 = " Regards\n"
    body6 = " Team Pocket Partner"
    body = body1 + body2 + body3 + body4 + body5 + body6
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(email, frmTable['email'], msg)
    # print('Email has been sent to '+email)

    server.quit()
