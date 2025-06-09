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
# scrape_to_file('https://www.gameshaventcg.com/search?page=1&q=%2Acultivate%2A', scraper_gh.gameshaven_scraper, "gameshaven_cultivate")
scrape_to_file('https://sg-manapro.com/collections/jumpstart-2022', scraper_mp.manapro_scraper, "manapro_jumpstart")