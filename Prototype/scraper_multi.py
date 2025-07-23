from bs4 import BeautifulSoup
import urllib.request
import json
import time
import re

lang_code_list = ["jp", "sp", "fr", "de", "it", "pt", "kr", "ru", "cs", "ct" ]
condition_dict = {"Near Mint": 1 , "Lightly Played": 2, "Moderately Played": 3, "Heavily Played": 4, "Damaged": 5 }

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
    actual_url = page.url
    if actual_url != url:
        print("URL error")
        print("actual url:", actual_url)
        return [], None

    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # empty_collection = soup.find("div", class_ = ["collection", "collection--empty"])
    # if  empty_collection != None:
    #     print(empty_collection)
    #     print("empty page")
    #     return [], None

    main_collection_product_grid = soup.find("ul",id="main-collection-product-grid")
    if main_collection_product_grid == None:
        print("empty page")
        return [], None
    
    product_list = main_collection_product_grid.find_all("script")
    link_list = soup.find("ul",id="main-collection-product-grid").find_all("div", class_ =["grid-view-item__link", "grid-view-item__image-container"])
    # print(product_list)

    cardlist = []
    for i in range(len(product_list)):
        out_of_stock = False
        # a = link_list[i].find("a")
        # print(a)
        # print(a.find("span"))
        # print("AAAAAAAAAAAAAAAAAAAAAAAAAA")
        if link_list[i].find("a").find("span", class_ = "outstock-overlay") != None:
            out_of_stock = True

        store_link = base_url + link_list[i].find("a")["href"]

        
        script = product_list[i].get_text().split('\n')
        script = script[2].strip("product = ,",)
        product = json.loads(script)

        if product["type"] != "MTG Single":
            continue

        # store_link = base_url + "/collections/mtg-singles-all-products/products/" + products["handle"]

        # name_list = products["title"].split("[",1)[0].split("(",1)[0]
        # for text in name_list:
        #     if text[-1] != "]" and text[-1] != ")":
        #         name = text
        #         break

        name = re.sub("[\(\[].*?[\)\]]", "", product["title"]).strip()
        

        variants = product["variants"]

        for card_json in variants:


            if card_json["available"]:
                card_dict = {"store": store_name}
                card_dict["store_id"] = card_json["id"]
                card_dict["name"] = name

                if card_json["sku"] != "" and card_json["sku"] != None:
                    card_dict["sku"] = card_json["sku"]
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

                    

                    
                else:
                    # print("Error missing SKU")
                    card_dict["sku"] = product["title"]

                    set_name_list = re.findall(r"\[(.*?)\]", product["title"] )
                    lang_list = re.findall(r"\((.*?)\)", product["title"] )

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
                        card_dict["bullshit"] = " , ".join(set_name_list[1:] + lang_list)
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
        

    # print(cardlist)
    if len(cardlist) == 0: #Whole page is out of stock 
        return cardlist, None #im just gonna asumme the rest is out of stock too

    next_page = soup.find("div", class_ = "pag_next").find("a") #next_page = None if there is no next page
    
    if next_page != None:
        next_page_url = base_url + next_page['href']
    else:
        next_page_url = None   
 
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

def onemtg_scrape_page(url):
    return template_scrape_page(url, "https://onemtg.com.sg", "One MTG")

def cardaffinity_scrape_page(url):
    return template_scrape_page(url, "https://card-affinity.com", "Card Affinity")

def cardboardcrackgames_scrape_page(url):
    return template_scrape_page(url, "https://www.cardboardcrackgames.com", "Cardboard Crack Games")

def flagshipgames_scrape_page(url):
    return template_scrape_page(url, "https://www.flagshipgames.sg", "Flagship Games")


def manapro_scrape_page(url):
    return template_scrape_page(url, 'https://sg-manapro.com/', "Mana Pro" )




def mtgasia_scraper(url):
    return template_scraper(url, "https://www.mtg-asia.com", "MTG Asia" )

def onemtg_scraper(url):
    return template_scraper(url, "https://onemtg.com.sg", "One MTG")


def cardaffinity_scraper(url):
    return template_scraper(url, "https://card-affinity.com", "Card Affinity")

def cardboardcrackgames_scraper(url):
    return template_scraper(url, "https://www.cardboardcrackgames.com", "Cardboard Crack Games")

def flagshipgames_scraper(url):
    return template_scraper(url, "https://www.flagshipgames.sg", "Flagship Games")



def manapro_scraper(url):
    return template_scraper(url, 'https://sg-manapro.com/', "Mana Pro" )

def manapro_get_all_scraper():
    first_url = "https://sg-manapro.com/collections/mtg-singles-all-products?page=1"
    second_url = "https://sg-manapro.com/collections/mtg-singles-all-products?sort_by=title-descending"
    # first_url = "https://sg-manapro.com/collections/mtg-singles-all-products/aether-revolt?page=8&sort_by=title-descending"
    # second_url = "https://sg-manapro.com/collections/mtg-singles-all-products/aether-revolt?page=2&sort_by=price-ascending"
    
    def manapro_all_scraper1():
        cardlist, next_url = manapro_scrape_page(manapro_all_scraper1.url )
        if next_url == None:
            manapro_all_scraper2.stop_id = cardlist[-1]["store_id"]
            return cardlist, manapro_all_scraper2
        else:
            manapro_all_scraper1.url = next_url
            return cardlist, manapro_all_scraper1
        

    manapro_all_scraper1.url = first_url
    
    def manapro_all_scraper2():
        cardlist, next_url = manapro_scrape_page(manapro_all_scraper2.url )

        for i in range(len(cardlist)):
            if cardlist[i]["store_id"] == manapro_all_scraper2.stop_id:
                cardlist = cardlist[:i]
                return cardlist, None
        

        if next_url == None:
            return cardlist, None
        else:
            manapro_all_scraper2.url = next_url
            return cardlist, manapro_all_scraper2
        


    manapro_all_scraper2.url = second_url

    return manapro_all_scraper1           
                            
# cardlist,url = template_scrape_page("https://onemtg.com.sg/search?options%5Bprefix%5D=last&page=8&q=cultivate&type=product", "https://onemtg.com.sg", "One MTG")


# cardlist,url = template_scrape_page("https://www.mtg-asia.com/search?type=product&options%5Bprefix%5D=last&q=cultivate", "https://www.mtg-asia.com", "MTG Asia" )


# cardlist,url = template_scrape_page("https://onemtg.com.sg/collections/all/phyrexian-soldier", "https://onemtg.com.sg", "One Asia" )
# print(cardlist)


# cardlist,url = manapro_scrape_page("https://sg-manapro.com/collections/mtg-singles-all-products?page=1")
# print(cardlist)


# onemtg_scrape_page("https://www.mtg-asia.com/collections/non-foil/edge-of-eternities-tokens")



# def get_collection_list():
#     out = []
#     url = "https://sg-manapro.com/collections/mtg-singles-all-products"

#     req = urllib.request.Request(url, data=None, 
#     headers={
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
#     }    )

#     page = urllib.request.urlopen(req)
#     time.sleep(0.5)
#     html = page.read().decode("utf-8")
#     soup = BeautifulSoup(html, "html.parser")

#     sort_tags = soup.find("div", id="SortTags") 
#     ul_list = sort_tags.find_all("ul")
#     # print(sort_tags)


#     set_name = sort_tags.find("ul", class_ = "SET_NAME")


#     a_list = set_name.find_all("a")
#     for a in a_list:
#         href = a["href"]
#         out.append(href)
    
#     print(out)


# get_collection_list()