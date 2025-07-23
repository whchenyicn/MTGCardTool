from bs4 import BeautifulSoup
import urllib.request
import json
import webpixel_scraper
import time
import re

lang_code_list = ["jp", "sp", "fr", "de", "it", "pt", "kr", "ru", "cs", "ct" ]
condition_dict = {"Near Mint": 1 , "Lightly Played": 2, "Moderately Played": 3, "Heavily Played": 4, "Damaged": 5 }


def cardcitadel_scrape_page(url):
    print(url)
    cardlist = []

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
    # img_to_sku = webpixel_scraper.get_img_dict(soup)

    link_to_sku = webpixel_scraper.get_link_dict(soup)
    # print(link_to_sku)
    # print(img_to_sku)

    out_of_stock = False

    product_list = soup.find_all("div", class_ ="product Norm")
    for product in product_list:
        
        buy_wrapper = product.find("div", class_ = "buyWrapper")
        if buy_wrapper == None:
            out_of_stock = True
            break

        title = product.find("p", class_ = "productTitle").text.strip()
        card_name = re.sub("[\(\[].*?[\)\]]", "", title).strip()
        


        # img = product.find("img")["src"].replace("_large","")
        link = product.find("div",class_ = "view").find("a")["href"].split("?")[0]
        if link[:32] == "/collections/mtg-singles-instock":
            link = link[32:]
        # print(link)

        sku = link_to_sku[link]
        if sku != None:
            sku_list = sku.split("-")
        if sku == None or len(sku_list) < 5:
            print("SKU Error:", sku)
            bullshit = "SKU Error"
            set = None
            col_number = None
            lang = None
        else:
            product_title = product.find("p", class_ = "productTitle").text
            sku = product_title
            set_name_list = re.findall(r"\[(.*?)\]", product_title )
            lang_list = re.findall(r"\((.*?)\)", product_title )

            set = set_name_list[0]
            col_number = None

            lang = "en"
            for s in lang_list:
                if len(s) == 2:
                    for lang_code in lang_code_list:
                        if s.lower() == lang_code:
                            lang = lang_code
                            lang_list.remove(s)
                            break
                else:
                    if "Japanese" in s:
                        lang = "jp"
                        break
            if len(set_name_list) > 1 or len(lang_list) > 0:
                bullshit = " , ".join(set_name_list + lang_list)
            else:
                bullshit = None




            bullshit = None
            set = sku_list[0].lower()
            col_number = sku_list[1].lower()
            lang = sku_list[-3].lower()
        

            if len(sku_list) > 5:
                bullshit = sku_list[2]
            else:
                bullshit = None

            
        
            

        variants = []

        for div in buy_wrapper.find_all("div", class_ ="addNow single"):
            addToCart_str = div["onclick"][10:-1] #removing "addToCart()""
            # print(addToCart_str)
            store_id, addToCart_str = addToCart_str.split(",", 1)  #isolating store id
            store_id = int(store_id.strip().strip("'") )

            # card_dict = {"store": "Cards Citadel","set": set, "col_number": col_number, "name": card_name, "bullshit": bullshit, "sku": sku, "lang": lang, "available":True, "store_link": "https://cardscitadel.com/" + link }
            
            card_dict = {"store": "Cards Citadel", "store_id": store_id, "name": card_name, "sku":sku, "set": set, "col_number": col_number, "lang": lang, "bullshit": bullshit }
            

            price_str = div.find("p").text

            
            # card_dict["store_id"] = int(store_id.strip().strip("'") )
            
            # print(addToCart_str)
            addToCart_str = addToCart_str.strip().strip("'")[len(title):].strip("- ")  #removing card name from str
            # print(addToCart_str)
            

            # print(card_dict["name"])
            # print(addToCart_str)
            # print(addToCart_str.split(" , ",1))
            condition_foil, addToCart_str = addToCart_str.split(",",1)

            condition_foil = condition_foil.strip("'")
            if condition_foil == "Default Title":
                continue
            card_dict["foil"] = condition_foil[-4:] == "Foil"
            if card_dict["foil"]:
                condition = condition_foil[:-5]
            else:
                condition = condition_foil
            card_dict["condition"] = condition_dict[condition]

            # print(price_str)
            price_str = price_str.split("-",1)[1].strip()
            # print(price_str)
            card_dict["price"] = int(price_str[1:-3] + price_str[-2:])
            # print(card_dict["price"])
            card_dict["available"] = True


            card_dict["quantity"] = int(   addToCart_str.split(",")[0].strip().strip("'")   )
            
            card_dict["store_link"] = "https://cardscitadel.com/" + link 
            cardlist.append(card_dict)

        

    pagination = soup.find("div", id = "pagination" )
    next_page = pagination.find_all("a")[-1]

    if len(next_page["class"]) == 2 and not out_of_stock:
        next_page_url = "https://cardscitadel.com/" + next_page["href"]
    else:
        next_page_url = None
    
    return cardlist,next_page_url



def cardcitadel_scraper(url):
    cardcitadel_cardlist = []
    while url != None:
        cardlist,url = cardcitadel_scrape_page(url)
        cardcitadel_cardlist.extend(cardlist)
        time.sleep(0.2)
    return cardcitadel_cardlist


def cardcitadel_get_all_scraper():
    first_url = "https://cardscitadel.com/collections/mtg-singles-instock?sort_by=title-ascending"
    second_url = "https://cardscitadel.com/collections/mtg-singles-instock?sort_by=title-descending"


    #for testing
    # first_url = "https://cardscitadel.com/collections/mtg-singles-instock/aether-revolt?page=14&sort_by=title-ascending"
    # second_url = "https://cardscitadel.com/collections/mtg-singles-instock/aether-revolt?page=1&sort_by=price-descending"
    
    def cardcitadel_all_scraper1():
        cardlist, next_url = cardcitadel_scrape_page(cardcitadel_all_scraper1.url )
        if next_url == None:
            cardcitadel_all_scraper2.stop_id = cardlist[-1]["store_id"]
            return cardlist, cardcitadel_all_scraper2
        else:
            cardcitadel_all_scraper1.url = next_url
            return cardlist, cardcitadel_all_scraper1
        

    cardcitadel_all_scraper1.url = first_url
    
    def cardcitadel_all_scraper2():
        cardlist, next_url = cardcitadel_scrape_page(cardcitadel_all_scraper2.url )

        for i in range(len(cardlist)):
            if cardlist[i]["store_id"] == cardcitadel_all_scraper2.stop_id:
                cardlist = cardlist[:i]
                return cardlist, None
        

        if next_url == None:
            return cardlist, None
        else:
            cardcitadel_all_scraper2.url = next_url
            return cardlist, cardcitadel_all_scraper2
        


    cardcitadel_all_scraper2.url = second_url

    return cardcitadel_all_scraper1

# last_page_url = "https://cardscitadel.com/search?page=8&q=%2Acultivate%2A"

# cardlist = cardcitadel_scraper("https://cardscitadel.com/search?q=*cultivate*")
# print(cardlist)
# cardcitadel_scrape_page(last_page_url)

# cardlist,url = cardcitadel_scrape_page("https://cardscitadel.com//collections/mtg-singles-instock?page=33&phcursor=eyJhbGciOiJIUzI1NiJ9.eyJzayI6InByb2R1Y3RfdGl0bGUiLCJzdiI6IkFpZCB0aGUgRmFsbGVuIFtXYXIgb2YgdGhlIFNwYXJrXSIsImQiOiJmIiwidWlkIjoyOTY4NDIxMDE3MjA3NiwibCI6MTIsIm8iOjAsInIiOiJDRFAiLCJ2IjoxLCJwIjozM30.x0KX1-NhPo91AZsIR_j6uLRrZ3K7PgDVgQJM-Trnhgg&sort_by=title-ascending")
# print(cardlist)