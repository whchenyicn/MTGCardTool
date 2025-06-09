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


def manapro_scrape_page(url):
    print(url)
    cardlist = []
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    #print(soup.prettify())
    product_list = soup.find("ul",id="main-collection-product-grid").find_all("script")
    for product in product_list:
        script = product.get_text()
        script = script.split('\n')
        script = script[2].strip("product = ,",)
        products = json.loads(script)
        variants = products["variants"]
        for variant in variants:
            #print(variant)
            name = variant['name']
            sku = variant['sku']
            price = variant['price']
            cardlist.append([name,sku,price])
        
    
        

#         name_set = product.find('p',class_="productTitle").get_text()
#         set = re.findall('\[(.*?)\]', name_set)[0].strip()
#         name = re.sub('\[(.*?)\]','', name_set).strip()

#         # print("Product")
#         # print(product.prettify())
#         # print("\n\n")
        

#         available_cards = product.find("div", class_= "hoverMask").find_all("div",class_="addNow single")
#         for card in available_cards:
#             quality_foil,price = card.p.get_text().split('-')
#             price = int(re.sub(r'[^0-9]', '', price))
#             quantity = card["onclick"].split(',')[-2]
#             if 'Foil' in quality_foil:
#                 foil = True
#                 quality = quality_foil.replace('Foil','').strip()
#             else:
#                 foil = False
#                 quality = quality_foil.strip()
            
            
#             # print("Card")
#             # print(card.prettify())
#             # print([name,set,quality,foil,price,quantity])
#             # print(foil)
#             # print("\n\n")
            
#             cardlist.append([name,set,quality,foil,price,quantity])
            
            
#         if len(available_cards) == 0:
#             cardlist.append([name,None,None,None,"Sold Out",0])
            
            
    next_page = soup.find("div",class_="pag_next").find_all("a")
    if len(next_page) > 0:
        next_page_url = 'https://sg-manapro.com/' + next_page[0]['href']
    else:
        next_page_url = None      
#         # print(name)
#         # print(price)
#         # print('\n\n')
    return cardlist,next_page_url


def manapro_scraper(url):
    manapro_cardlist = []
    while url != None:
        cardlist,url = manapro_scrape_page(url)
        manapro_cardlist.extend(cardlist)

    return manapro_cardlist

#url = 'https://sg-manapro.com/collections/jumpstart-2022'
#url = 'https://sg-manapro.com/collections/mtg-singles-all-products'
#manapro_cardlist = manapro_scraper(url)
#write_to_file('manapro_cardlist.csv',manapro_cardlist)





def scrape_to_file(url ,scraper, filename):
    cardlist = scraper(url)
    if type(cardlist[0]) == type([0]):
        write_to_csv_file(filename + ".csv" ,cardlist)
    else:
        write_to_json_file(filename + ".json" ,cardlist)

        
# scrape_to_file('https://agorahobby.com/store/search?category=mtg&searchfield=lightning', scraper_ah.agorahobby_scraper, "agorahobby_lightning")
# scrape_to_file('https://www.greyogregames.com/search?q=*rhystic+study*' , scraper_gog.greyogregames_scraper, "greyogregames_rhystic")
# scrape_to_file('https://www.greyogregames.com/search?q=*lightning*' , scraper_gog.greyogregames_scraper, "greyogregames_lightning")
scrape_to_file('https://www.gameshaventcg.com/search?page=1&q=%2Acultivate%2A', scraper_gh.gameshaven_scraper, "gameshaven_cultivate")