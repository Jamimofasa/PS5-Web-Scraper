import time

from bs4 import BeautifulSoup
import requests
import smtplib

# Amazon URL to be scraped
# url = "https://www.amazon.com/PlayStation-5-Console/dp/B09DFCB66S?ref_=ast_sto_dp"
# Testing second URL link
# url = "https://www.amazon.com/dp/B08YSY9PSH/ref=sspa_dk_detail_3?psc=1&pd_rd_i=B08YSY9PSH&pd_rd_w=OU1Io&pf_rd_p=9fd3ea7c-b77c-42ac-b43b-c872d3f37c38&pd_rd_wg=snCOe&pf_rd_r=H5ZFKD472FJVY37BK93G&pd_rd_r=c23b406f-0f93-49f6-94b3-75310e92d651&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFDVVZWOEo4SU5BNk0mZW5jcnlwdGVkSWQ9QTA3NDkzNzhEMUY2M0E4RERZQk4mZW5jcnlwdGVkQWRJZD1BMDc1OTU5NjFaVU5POTBJT0ZHUFUmd2lkZ2V0TmFtZT1zcF9kZXRhaWwmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl"
# Bad URL link
# url = "https://www.amazon.com/PlayStaton-5-Console/dp/B09DFCB6S?ref_=ast_sto_dp"


# Best Buy URL to be scraped
# url ="https://www.bestbuy.com/site/playstation-5/ps5-consoles/pcmcat1587395025973.c?id=pcmcat1587395025973"
# Best Buy testing second link
# url = "https://www.bestbuy.com/site/searchpage.jsp?st=xbox&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys"


# Change Header for browser that you prefer I'm using Mozilla Firefox
# Header from http://myhttpheader.com/
headers = {'Accept-Language': "en-US,en;q=0.5", 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"}

# Send an email using Smtp(Simple Mail Transfer Protocol)

# fill in with email login info and who your sending to
user =""
password = ""
fromEmailAddress=""
sendingToEmailAddress=""
smtp_server =""
port = 587
# Choose one below
# Gmail: smtp.gmail.com port: 25
# Hotmail: smtp.live.com port: 587
# Outlook: outlook.office365.com
# Yahoo: smtp.mail.yahoo.com
# If you use another email provider, just Google for your email provider e.g. "Gmail SMTP address"
# Gmail will need to change security for apps

def sendEmail(message):


    # create a connection
    with smtplib.SMTP(smtp_server,port) as connection:

        # Start connection and secure it
        connection.starttls()
        connection.login(user=user,password=password)
        connection.sendmail(from_addr=fromEmailAddress,to_addrs=sendingToEmailAddress, msg=f'Subject:PS5 InStock\n\n {message}')
        connection.close()



def amazonScraper(url):

    try:
        page = requests.get(url, headers = headers)

        if not page:
            raise Exception

    except Exception:
        # Change to log
        print(f'Error: Bad Amazon URL Link\n{url}\n')

    else:
        # use html.parser to load contents of web page
        soup = BeautifulSoup(page.content, "html.parser")

        # Check to see if in stock
        availability = soup.find(id="availability")

        # Check for Price
        buy_box = soup.find("div", id="buybox")
        price = buy_box.find(class_="a-offscreen")

        # Check if Out-Of-Stock
        outOfStock = buy_box.find("div", id="outOfStock")

        # if there is stock send an email
        # Include in email: item, In stock / count(if available), and price
        if not outOfStock:
          message = f'{soup.title.text}\n{availability.text.strip()}\n{price.text}\n{url}'
          # print(message)
          sendEmail(message)



def bestBuyScraper(url):

    try:
        page = requests.get(url, headers = headers)

        if not page:
            raise Exception

    except Exception:
        # Change to log
        print(f'Error: Bad Best Buy URL Link\n{url}\n')

    else:
        # use html.parser to load contents of web page
        soup = BeautifulSoup(page.content, "html.parser")

        # find container of items on bestbuy page
        available = soup.find(class_="pl-page-content")

        # search for all the items in the list("li")
        list = available.find_all("li", class_="sku-item")

        # go through each item container
        for item in list:

            # Look for each button if button is "Add to Cart" or "Find A Store" on bestbuy page
            button = item.find("button", class_="c-button c-button-primary c-button-sm c-button-block c-button-icon c-button-icon-leading add-to-cart-button")  \
                     or item.find("button", class_="c-button c-button-secondary c-button-sm c-button-block add-to-cart-button")


            # If not sold out email item with price
            if button and  item.find(class_="sr-only"):
                item_name = item.find("h4", class_="sku-header")
                link = item_name.find( href = True)

                price = item.find(class_="sr-only")

                # message = f"{item_name.text.strip()}\n{price.text.strip()}\n https://www.bestbuy.com{link['href']}\n"
                message = f"https://www.bestbuy.com{link['href']}\n"

                # email message
                # print(message)
                sendEmail(message)
                time.sleep(1)

