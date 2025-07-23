
from bs4 import BeautifulSoup
import urllib.request
import json
import time
import re

lang_code_list = ["jp", "sp", "fr", "de", "it", "pt", "kr", "ru", "cs", "ct" ]
condition_dict = {"Near Mint": 1 , "Lightly Played": 2, "Moderately Played": 3, "Heavily Played": 4, "Damaged": 5 }


def template_scrape_page(url, base_url, store_name):
    
    print(url)

    # Exception testing
    # if url == "https://www.flagshipgames.sg/search?type=product&options%5Bprefix%5D=last&q=" + "30th-anniversary-edition":
    #     raise Exception

    if store_name == "Flagship Games":
        offset = 1
    else:
        offset = 0

    req = urllib.request.Request(url, data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }    )

    page = urllib.request.urlopen(req)
    actual_url = page.url
    if actual_url != url:
        print("URL error")
        print("actual url:", actual_url)
        return [], None

    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    product_list = soup.find("div", class_ = ["list-view-items", "products-display"]).find_all(attrs={"data-product-variants": True})
    link_list = soup.find("div", class_ = ["list-view-items", "products-display"]).find_all(class_ = "grid-view-item")
    # print(product_list)

    out_of_stock = False
    cardlist = []
    for i in range(len(product_list)):
        card = product_list[i]
        if card["data-product-type"] != "MTG Single":
            continue
        
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
                card_dict = {"store": store_name}
                card_dict["store_id"] = card_json["id"]
                card_dict["name"] = re.sub("[\(\[].*?[\)\]]", "", card_json["name"][:- len(card_json["option1"])] ).strip(" -")


                if card_json["sku"] != "" and card_json["sku"] != None and "undefined" not in card_json["sku"]:
                    
                    sku = card_json["sku"].split("-")
                    card_dict["sku"] = card_json["sku"]

                    card_dict["set"] = sku[0].lower()
                    card_dict["col_number"] = sku[1].lower()
                    
                    card_dict["lang"] = sku[-3].lower()
                    
                    if len(sku) > 5:
                        card_dict["bullshit"] = sku[2]
                    else:
                        card_dict["bullshit"] = None
                    
                    # card_dict["foil"] = (sku[-2] == "FO")
                    # card_dict["condition"] = int(sku[-1]) + offset

                    condition_foil = card_json["option1"]
                    card_dict["foil"] = condition_foil[-4:] == "Foil"
                    if card_dict["foil"]:
                        condition = condition_foil[:-5]
                    else:
                        condition = condition_foil
                    card_dict["condition"] = condition_dict[condition]

                    
                else:
                    print("Error missing SKU")
                    card_dict["sku"] = card_json["name"]

                    set_name_list = re.findall(r"\[(.*?)\]", card_json["name"] )
                    lang_list = re.findall(r"\((.*?)\)", card_json["name"] )

                    card_dict["set"] = set_name_list[0]
                    card_dict["col_number"] = None

                    card_dict["lang"] = "en"
                    for s in lang_list:
                        if len(s) == 2:
                            for lang_code in lang_code_list:
                                if s.lower() == lang_code:
                                    card_dict["lang"] = lang_code
                                    lang_list.remove(s)
                                    break
                        else:
                            if "Japanese" in s:
                                card_dict["lang"] = "jp"
                                break
                    if len(set_name_list) > 1 or len(lang_list) > 0:
                        card_dict["bullshit"] = " , ".join(set_name_list + lang_list)
                    else:
                        card_dict["bullshit"] = None
                    
                    condition_foil = card_json["option1"]
                    card_dict["foil"] = condition_foil[-4:] == "Foil"
                    if card_dict["foil"]:
                        condition = condition_foil[:-5]
                    else:
                        condition = condition_foil
                    card_dict["condition"] = condition_dict[condition]


                card_dict["price"] = card_json["price"]
                card_dict["available"] = card_json["available"]
                card_dict["quantity"] = None
                card_dict["store_link"] = store_link

                cardlist.append(card_dict)
            
            else:
                break
        
        if out_of_stock:
            break

    # print(cardlist)


    next_page = soup.find("div", class_ = "pag_next") #next_page = None if this is last page

    if next_page == None or out_of_stock:
        next_page_url = None  
    else:
        next_page_a = next_page.find("a") #next_page_a = None if there is only one page
        if next_page_a == None:
            next_page_url = None  
        else:
            next_page_url = base_url + next_page_a['href']
  
 
    return cardlist,next_page_url


# def get_scrape_page(base_url, store_name):
#     def scrape_page(url):
#         return template_scrape_page(url, base_url, store_name)
    
#     return scrape_page

def template_scraper(url, base_url, store_name):
    out = []
    while url != None:
        cardlist,url = template_scrape_page(url, base_url, store_name)
        out.extend(cardlist)
        # print(len(mtgasia_cardlist))
        time.sleep(0.1)

    return out


def mtgasia_scrape_page(url):
    return template_scrape_page(url, "https://www.mtg-asia.com", "MTG Asia")

def cardaffinity_scrape_page(url):
    return template_scrape_page(url, "https://card-affinity.com", "Card Affinity")

def cardboardcrackgames_scrape_page(url):
    return template_scrape_page(url, "https://www.cardboardcrackgames.com", "Cardboard Crack Games")

def flagshipgames_scrape_page(url):
    return template_scrape_page(url, "https://www.flagshipgames.sg", "Flagship Games")

def onemtg_scrape_page(url):
    return template_scrape_page(url, "https://onemtg.com.sg", "One MTG")

def manapro_scrape_page(url):
    return template_scrape_page(url, 'https://sg-manapro.com/', "Mana Pro" )




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



# cardlist,url = flagshipgames_scrape_page("https://www.flagshipgames.sg/search?type=product&options%5Bprefix%5D=last&q=15th-anniversary")
# print(cardlist)
