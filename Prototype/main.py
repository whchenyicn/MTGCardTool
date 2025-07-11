from bs4 import BeautifulSoup
import urllib.request
from urllib.request import urlopen
import urllib
import re
import csv
import json

#local imports
# import scraper_gog as scraper_gog
import scraper_ah
import scraper_ml
import scraper_cc
import scraper_dp
import scraper_multi
import scraper_multi2


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

# scrape_to_file('https://www.greyogregames.com/search?page=1&q=%2Acultivate%2A' , scraper_multi2.greyogregames_scraper, "greyogregames_cultivate")
# scrape_to_file('https://www.greyogregames.com/search?q=*lightning*' , scraper_multi2.greyogregames_scraper, "greyogregames_lightning")

# scrape_to_file('https://www.gameshaventcg.com/search?page=1&q=%2Acultivate%2A', scraper_multi2.gameshaven_scraper, "gameshaven_cultivatate")


# scrape_to_file("https://hideoutcg.com/search?page=1&q=%2Acultivate%2A", scraper_multi2.hideout_scraper, "hideout_cultivate")


# scrape_to_file('https://sg-manapro.com/collections/jumpstart-2022', scraper_mp.manapro_scraper, "manapro_jumpstart")
# scrape_to_file('https://sg-manapro.com/search?type=product&options%5Bprefix%5D=last&q=barone', scraper_multi.manapro_scraper, "manapro_barone")

# scrape_to_file("https://www.moxandlotus.sg/products?title=lightning", scraper_ml.moxandlotus_scraper, "moxandlotus_lightning")
#STILL NOT WORKING

# scrape_to_file("https://onemtg.com.sg/search?type=product&options%5Bprefix%5D=last&q=cultivate", scraper_multi.onemtg_scraper , "onemtg_cultivate" )
# scrape_to_file("https://www.mtg-asia.com/search?options%5Bprefix%5D=last&page=1&q=cultivate&type=product", scraper_multi.mtgasia_scraper , "mtgasia_cultivate" )
# scrape_to_file("https://card-affinity.com/search?type=product&options%5Bprefix%5D=last&q=cultivate", scraper_multi.cardaffinity_scraper , "cardaffinity_cultivate" )
# scrape_to_file("https://www.cardboardcrackgames.com/search?type=product&options%5Bprefix%5D=last&q=cultivate", scraper_multi.cardboardcrackgames_scraper , "cardboardcrackgames_cultivate" )
# scrape_to_file("https://www.flagshipgames.sg/search?type=product&options%5Bprefix%5D=last&q=cultivate", scraper_multi.flagshipgames_scraper , "flagshipgames_cultivate" )


# scrape_to_file("https://cardscitadel.com/search?q=*cultivate*", scraper_cc.cardcitadel_scraper , "cardcitadel_cultivate" )

# scrape_to_file("https://www.duellerspoint.com/products/search?utf8=%E2%9C%93&search_text=cultivate", scraper_dp.duellerspoint_scraper , "duellerspoint_cultivate")