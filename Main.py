import WebScraper as scraper
import time

def main():

    while(True):
        scraper.amazonScraper("https://www.amazon.com/PlayStation-5-Console/dp/B09DFCB66S?ref_=ast_sto_dp")
        scraper.bestBuyScraper("https://www.bestbuy.com/site/playstation-5/ps5-consoles/pcmcat1587395025973.c?id=pcmcat1587395025973")
        # sleep for 5 seconds
        time.sleep(5)



if __name__ == "__main__":
    main()