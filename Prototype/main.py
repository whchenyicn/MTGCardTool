from bs4 import BeautifulSoup
import urllib.request
from urllib.request import urlopen
import urllib
import re
import csv
import json

#local imports
import scraper_gog as scraper_gog
import scraper_ah
import scraper_gh
import scraper_mp
import scraper_ml
import scraper_mtga
import scraper_omtg
import scraper_ca
import scraper_cc
import scraper_h


def write_to_csv_file(filename,nestedlist):
    with open(filename,'w',encoding="utf-8", newline='') as f:
        csv_writer = csv.writer(f)
        for listing in nestedlist:
            csv_writer.writerow(listing)
            # print(listing)

def write_to_json_file(filename,dictlist):
    with open(filename,'w',encoding="utf-8", newline='') as f:
        for listing in dictlist:
            json_object = json.dumps(listing, indent=4)
            f.write(json_object)
            
            # print(listing)

def scrape_to_file(url ,scraper, filename):
    cardlist = scraper(url)
    if type(cardlist[0]) == type([0]):
        write_to_csv_file(filename + ".csv" ,cardlist)
    else:
        write_to_json_file(filename + ".json" ,cardlist)

        
# scrape_to_file('https://agorahobby.com/store/search?category=mtg&searchfield=lightning', scraper_ah.agorahobby_scraper, "agorahobby_lightning")

# scrape_to_file('https://www.greyogregames.com/search?q=*rhystic+study*' , scraper_gog.greyogregames_scraper, "greyogregames_rhystic")
# scrape_to_file('https://www.greyogregames.com/search?q=*lightning*' , scraper_gog.greyogregames_scraper, "greyogregames_lightning")

# scrape_to_file('https://www.gameshaventcg.com/search?page=1&q=%2Acultivate%2A', scraper_gh.gameshaven_scraper, "gameshaven_cultivate_notwebpixel")


# scrape_to_file('https://www.gameshaventcg.com/search?page=1&q=%2Acultivate%2A', scraper_h.hideout_scraper, "hideout_cultivate")

# scrape_to_file('https://sg-manapro.com/collections/jumpstart-2022', scraper_mp.manapro_scraper, "manapro_jumpstart")
# scrape_to_file('https://sg-manapro.com/search?type=product&options%5Bprefix%5D=last&q=barone', scraper_mp.manapro_scraper, "manapro_barone_notwebpixel")

# scrape_to_file("https://www.moxandlotus.sg/products?title=lightning", scraper_ml.moxandlotus_scraper, "moxandlotus_lightning")
#STILL NOT WORKING

# scrape_to_file("https://www.mtg-asia.com/search?options%5Bprefix%5D=last&page=1&q=cultivate&type=product", scraper_mtga.mtgasia_scraper , "mtgasia_cultivate" )

# scrape_to_file("https://onemtg.com.sg/search?type=product&options%5Bprefix%5D=last&q=cultivate", scraper_omtg.onemtg_scraper , "onemtg_cultivate" )

# scrape_to_file("https://card-affinity.com/search?type=product&options%5Bprefix%5D=last&q=cultivate", scraper_ca.cardaffinity_scraper , "cardaffinity_cultivate" )

# scrape_to_file("https://cardscitadel.com/search?q=*cultivate*", scraper_cc.cardcitadel_scraper , "cardcitadel_cultivate" )