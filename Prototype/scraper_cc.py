from bs4 import BeautifulSoup
import urllib.request
import json
import webpixel_scraper
import time

condition_dict = {"Near Mint": 1 , "Lightly Played": 2, "Moderately Played": 3, "Heavily Played": 4, "Damaged": 5 }

def cardcitadel_scrape_page(url):
    print(url)
    cardlist = []

    req = urllib.request.Request(url, data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }    )

    page = urllib.request.urlopen(req)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    # img_to_sku = webpixel_scraper.get_img_dict(soup)

    link_to_sku = webpixel_scraper.get_link_dict(soup)
    # print(img_to_sku)

    out_of_stock = False

    product_list = soup.find_all("div", class_ ="product Norm")
    for product in product_list:
        
        buy_wrapper = product.find("div", class_ = "buyWrapper")
        if buy_wrapper == None:
            out_of_stock = True
            break


        # img = product.find("img")["src"].replace("_large","")
        link = product.find("div",class_ = "view").find("a")["href"].split("?")[0]

        sku = link_to_sku[link].split("-")
        if len(sku) < 5:
            print("SKU Error:", sku)
            continue
        bullshit = None
        set = sku[0].lower()
        col_number = sku[1].lower()
        lang = sku[-3].lower()

        if len(sku) > 5:
            bullshit = sku[2]
        else:
            bullshit = None
            

        variants = []

        for div in buy_wrapper.find_all("div", class_ ="addNow single"):
            card_dict = {"store": "Cards Citadel","set": set, "col_number": col_number, "bullshit": bullshit, "lang": lang, "store_link": "https://cardscitadel.com/" + link }
            addToCart_str = div["onclick"][11:-1] #removing "addToCart()""
            card_dict["store_id"], addToCart_str = addToCart_str.split("','", 1)  #isolating store id

            addToCart_str = addToCart_str.split(" - ", 1)[1]  #removing card name from str
            condition_foil, addToCart_str = addToCart_str.split("','",1)
            card_dict["foil"] = condition_foil[-4:] == "Foil"
            if card_dict["foil"]:
                condition = condition_foil[:-5]
            else:
                condition = condition_foil
            card_dict["condition"] = condition_dict[condition]
            card_dict["quantity"] = int(addToCart_str[:-3])

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

# last_page_url = "https://cardscitadel.com/search?page=8&q=%2Acultivate%2A"

# cardlist = cardcitadel_scraper("https://cardscitadel.com/search?q=*cultivate*")
# print(cardlist)
# cardcitadel_scrape_page(last_page_url)
