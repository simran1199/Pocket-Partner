import requests
import smtplib

if (price>1400):              //price need to be fetched by scaping, normally added right now
    send_mail()

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('shrishtisrivastava04@gmail.com','mkfhsgdruyutjkmsak')

    subject ="Heyy !!!...The price fell down, grab your favourites now !!!"
    body ='Check the amazon link'

    msg =f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'shrishtisrivastava04@gmail.com',
        msg
    )
    print('Email has been sent')

    server.quit()

