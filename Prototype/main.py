from bs4 import BeautifulSoup
import urllib.request
from urllib.request import urlopen
import urllib
import re
import csv
import json


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

#url = 'https://www.greyogregames.com/search?q=*rhystic+study*'
#url = 'https://www.greyogregames.com/search?q=*kogla*'
#url = 'https://www.greyogregames.com/collections/mtg-singles-all-products'

def greyogregames_scrape_page(url):
    print(url)
    req = urllib.request.Request(url, data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }    )

    page = urlopen(req)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    script = soup.find("script", id = "web-pixels-manager-setup") #directly obtains info from the sites script

    start = "\"productVariants\":"
    end = "}});},"
    z = script.text
    z1 = z[z.find(start)+len(start):z.rfind(end)].strip()
    json_dirty = z1[z1.find(start)+len(start):].strip() 
    #finds the portion of the script containing the json with all the cards information

    #there are 2 instances of the string start in the script 
    #so it runs the search twice to get the second instance

    cardlist = json.loads(json_dirty) #parse into json
            

    next_page = soup.find("ol", class_ = "pagination").contents[-1].find("a") #next_page = None if there is no next page

    if next_page != None:
        next_page_url = 'https://www.greyogregames.com/' + next_page['href']
    else:
        next_page_url = None   
 
    return cardlist,next_page_url




def greyogregames_scraper(url):
    greyogregames_cardlist = []
    while url != None:
        cardlist,url = greyogregames_scrape_page(url)
        greyogregames_cardlist.extend(cardlist)

    return greyogregames_cardlist




# greyogregames_cardlist = greyogregames_scraper(url)
# write_to_file("greyogregames_cardlist.csv",greyogregames_cardlist)
# print(greyogregames_cardlist)

# url = "https://cardscitadel.com/search?q=*cultivate*"
# cardcitadel_cardlist = greyogregames_scraper(url)
# print(cardcitadel_cardlist)
# write_to_file("cardcitadel_cardlist.csv",cardcitadel_cardlist)

# url = "https://sanctuary-gaming.com/search?q=*cultivate*"
# sanctuarygaming_cardlist = greyogregames_scraper(url)
# print(sanctuarygaming_cardlist)
# write_to_file("sanctuarygaming_cardlist.csv",sanctuarygaming_cardlist)

# url = "https://www.flagshipgames.sg/search?q=*cultivate*"
# flagshipgames_cardlist = greyogregames_scraper(url)
# print(flagshipgames_cardlist)
# write_to_file("flagshipgames_cardlist.csv",flagshipgames_cardlist)


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



def gameshaven_scrape_page(url):
    print(url)
    cardlist = []
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    product_list = soup.find_all("div",class_="productCard__card")
    for product in product_list:
        
        productCard_lower = product.find('div',class_="productCard__lower")
        name = productCard_lower.find('p',class_="productCard__title").get_text().strip()
        set = productCard_lower.find('p',class_="productCard__setName").get_text()
        
        available_cards = productCard_lower.find("ul", class_= "productChip__grid").find_all("li")
        for card in available_cards:
            if card['data-variantavailable'] == 'true':
                quantity = card['data-variantqty']
                price = card['data-variantprice']
                condition_foil = card['data-varianttitle']
                
                if 'Foil' in condition_foil:
                    foil = True
                    condition = condition_foil.replace('Foil','').strip()
                else:
                    foil = False
                    condition = condition_foil.strip()
                    
                cardlist.append([name,set,condition,foil,price,quantity])
      
    pagination = soup.find("ol",class_="pagination")
    next_page = pagination.find_all("li")[-1]
    if next_page.has_attr('class'):
        next_page_url = None
    else:
        next_page_url = 'https://www.gameshaventcg.com/' + next_page.a['href']
    return cardlist,next_page_url

def gameshaven_scraper(url):
    gameshaven_cardlist = []
    while url != None:
        cardlist,url = gameshaven_scrape_page(url)
        gameshaven_cardlist.extend(cardlist)

    return gameshaven_cardlist

#url = "https://www.gameshaventcg.com/search?page=1&q=%2A%2A"
# url = 'https://www.gameshaventcg.com/search?page=1&q=%2Acultivate%2A'
#url = 'https://www.gameshaventcg.com/collections/gh-standard-cards'
#gameshaven_cardlist = gameshaven_scraper(url)
#print(gameshaven_cardlist)
#write_to_file('gameshaven_cardlist.csv',gameshaven_cardlist)

def agorahobby_scrape_page(url):
    print(url)
    cardlist = []
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    product_list = soup.find_all("div",class_="store-item")
    for product in product_list:
        script = product.find('script',type="text/javascript").get_text()
        script = re.findall('=(.*?);', script)[2]
        product_info = json.loads(script)
        if len(product_info['stock']) != 1:
            raise Exception('bruh')
        sku = product_info['stock'][0]['sku']
        quantity = product_info['stock'][0]['stock_level']
        price = product_info['price']
        regular_price = product_info['regular_price']
        sale_price = product_info['sale_price']
        title = product.find('div',class_="store-item-title").get_text()
        
        cardlist.append([title,sku,quantity,price,regular_price,sale_price])
    
    next_page = soup.find_all("a",class_="page-next")
    if len(next_page) > 0:
        next_page_url = next_page[0]['href']
    else:
        next_page_url = None
    
    return cardlist,next_page_url

def agorahobby_scraper(url):
    agorahobby_cardlist = []
    while url != None:
        cardlist,url = agorahobby_scrape_page(url)
        agorahobby_cardlist.extend(cardlist)

    return agorahobby_cardlist

# url = 'https://agorahobby.com/store/search?category=mtg&searchfield=lightning+bolt'
#searching for lightning bolt doesnt work for some reason but cultivate does


#url = 'https://agorahobby.com/store/search?category=mtg&searchfield=cultivate&search=GO'
#url = 'https://agorahobby.com/store/search?category=mtg&searchfield=b&search=GO'
#agorahobby_cardlist = agorahobby_scraper(url)
#write_to_file('agorahobby_cardlist.csv',agorahobby_cardlist)


def scrape_to_file(url ,scraper, filename):
    cardlist = scraper(url)
    if type(cardlist[0]) == type([0]):
        write_to_csv_file(filename,cardlist)
    else:
        write_to_json_file(filename,cardlist)

        
# scrape_to_file('https://agorahobby.com/store/search?category=mtg&searchfield=lightning', agorahobby_scraper, "agorahobby_lightning.csv")
# scrape_to_file('https://www.greyogregames.com/search?q=*rhystic+study*' , greyogregames_scraper, "greyogregames_rhystic.csv")
scrape_to_file('https://www.greyogregames.com/search?q=*lightning*' , greyogregames_scraper, "greyogregames_lightning.csv")