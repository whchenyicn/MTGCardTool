
from bs4 import BeautifulSoup
import urllib.request
import json
import time

def template_scrape_page(url, base_url, store_name):
    print(url)
    if store_name == "Flagship Games":
        offset = 1
    else:
        offset = 0

    req = urllib.request.Request(url, data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }    )

    page = urllib.request.urlopen(req)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    product_list = soup.find("div", class_ = ["list-view-items", "products-display"]).find_all(attrs={"data-product-variants": True})
    link_list = soup.find("div", class_ = ["list-view-items", "products-display"]).find_all(class_ = "grid-view-item")
    # print(product_list)

    out_of_stock = False
    cardlist = []
    for i in range(len(product_list)):
        card = product_list[i]

        # a = link_list[i].find("a")
        # print(a)
        # print(a.find("span"))
        # print("AAAAAAAAAAAAAAAAAAAAAAAAAA")
        # if link_list[i].find("a").find("span", class_ = "outstock-overlay") != None:
        #     out_of_stock = True

        store_link = base_url + link_list[i].find("a")["href"]

        out_of_stock = True
        for card_json in json.loads(card["data-product-variants"]):
            if card_json["available"]:
                out_of_stock = False
                if not card_json["sku"] == "":
                    card_dict = {"store": store_name}
                    card_dict["store_id"] = card_json["id"]
                    sku = card_json["sku"].split("-")
                    card_dict["set"] = sku[0].lower()
                    card_dict["col_number"] = sku[1].lower()
                    if len(sku) > 5:
                        card_dict["bullshit"] = sku[2]
                    else:
                        card_dict["bullshit"] = None

                    card_dict["lang"] = sku[-3].lower()
                    
                    card_dict["foil"] = (sku[-2] == "FO")
                    card_dict["condition"] = int(sku[-1]) + offset

                    

                    card_dict["price"] = card_json["price"]
                    card_dict["available"] = card_json["available"]
                    card_dict["quantity"] = None
                    card_dict["store_link"] = store_link

                    cardlist.append(card_dict)
                if card_json["sku"] == "":
                    print("Error missing SKU")
            
        
        if out_of_stock:
            break

    # print(cardlist)


    next_page = soup.find("div", class_ = "pag_next").find("a") #next_page = None if there is no next page
    
    if next_page != None and not out_of_stock:
        next_page_url = base_url + next_page['href']
    else:
        next_page_url = None   
 
    return cardlist,next_page_url




def template_scraper(url, base_url, store_name):
    out = []
    while url != None:
        cardlist,url = template_scrape_page(url, base_url, store_name)
        out.extend(cardlist)
        # print(len(mtgasia_cardlist))
        time.sleep(0.1)

    return out

def mtgasia_scraper(url):
    return template_scraper(url, "https://www.mtg-asia.com", "MTG Asia" )

def cardaffinity_scraper(url):
    return template_scraper(url, "https://card-affinity.com", "Card Affinity")

def cardboardcrackgames_scraper(url):
    return template_scraper(url, "https://www.cardboardcrackgames.com", "Cardboard Crack Games")

def flagshipgames_scraper(url):
    return template_scraper(url, "https://www.flagshipgames.sg", "Flagship Games")

def onemtg_scraper(url):
    return template_scraper(url, "https://onemtg.com.sg", "One MTG")

def manapro_scraper(url):
    return template_scraper(url, 'https://sg-manapro.com/', "Mana Pro" )
                            
                            
# cardlist,url = template_scrape_page("https://onemtg.com.sg/search?options%5Bprefix%5D=last&page=8&q=cultivate&type=product", "https://onemtg.com.sg", "One MTG")


# cardlist,url = template_scrape_page("https://www.mtg-asia.com/search?type=product&options%5Bprefix%5D=last&q=cultivate", "https://www.mtg-asia.com", "MTG Asia" )


# cardlist,url = template_scrape_page("https://onemtg.com.sg/collections/all/phyrexian-soldier", "https://onemtg.com.sg", "One Asia" )
# print(cardlist)