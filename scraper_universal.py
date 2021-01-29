import requests
from bs4 import BeautifulSoup
import smtplib
import time

URL = 'https://www.megaknihy.cz/unikove-hry/286040-escape-room-unikova-hra-exit.html?search_pos=2'
# google for "my user agent" and copy result here
headers = {"User-Agent": 'YOUR_DATA_HERE'}

def check_price():
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup.prettify()) # print in console all page content
    title = soup.find(itemprop="name").get_text().strip() #.strip() removes empty spaces
    # get the first child of the element with id="our_price_display" (it contains 2 spans)
    price = soup.find(id="our_price_display").find("span", recursive=False).get_text()
    print(title)
    print(f"{price} CZK")
    if (int(price) < 700): # use higher value to test it, e. g. 800
        send_mail(title, price)

def send_mail(title, price):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
# set 2 factor authentification on gmail and generate an app password
    server.login("YOUR_EMAIL@gmail.com", "YOUR_GOOGLE_APP_PASSWORD")
    subject = f"{title}: {price} CZK only!"
    body = f"Check the {title}, the price is {price} CZK only: {URL}"

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(            # from, to, message
        "SENDER@GMAIL.COM",
        "RECIPIENT@GMAIL.COM",
        msg.encode('utf-8') # was getting an error "'ascii' code can't encode character '\xda'" => encoding solved it
    )

    print("Email sent.")

    server.quit()

while(True):
    check_price()
    time.sleep(3600) # check price once a hour



