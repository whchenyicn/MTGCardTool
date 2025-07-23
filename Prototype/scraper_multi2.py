from bs4 import BeautifulSoup
import urllib.request
import json
import webpixel_scraper
import time

condition_dict = {"Near Mint": 1 , "Lightly Played": 2, "Moderately Played": 3, "Heavily Played": 4, "Damaged": 5 }


def template_scrape_page(url, base_url, store_name):
    print(url)
    cardlist = []
    
    req = urllib.request.Request(url, data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    } 
    )
    page = urllib.request.urlopen(req)
    actual_url = page.url
    
    if actual_url != url:

        print("URL error")
        print("actual url:", actual_url)
        return [], None

    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # soup = get_soup.get_soup_proxy(url)
    # soup = get_soup.get_soup(url)
    id_to_sku = webpixel_scraper.get_id_dict(soup)
    # print(id_to_sku)

    out_of_stock = True

    product_list = soup.find_all("div", **{"class_" :"productCard__card", "data-producttype" : "MTG Single"} )

    for product in product_list:
        if product.find("form") == None:
            continue
        else:
            out_of_stock = False
        

        store_link = base_url + product.find("a")["href"]

        productCard_lower = product.find('div',class_="productCard__lower")
        name = productCard_lower.find('p',class_="productCard__title").get_text().strip()
        # set = productCard_lower.find('p',class_="productCard__setName").get_text()
        
        available_cards = productCard_lower.find("ul", class_= "productChip__grid").find_all("li")
        first_card = available_cards[0]
        sku = id_to_sku[first_card["onclick"][14:-1].split(',')[1].strip("/' ")]
        if sku != None:
            sku_list = sku.split("-")
        sku_list = sku.split("-")
        if sku == None or len(sku_list) < 5:
            print("SKU Error:", sku)
            bullshit = "SKU Error"
            set = None
            col_number = None
            lang = None
        else:
            bullshit = None
            set = sku_list[0].lower()
            col_number = sku_list[1].lower()
            lang = sku_list[-3].lower()

            if len(sku_list) > 5:
                bullshit = sku_list[2]
            else:
                bullshit = None

        for card in available_cards:
            if card['data-variantavailable'] == 'true':
                store_id = int(card["onclick"][14:-1].split(',')[1].strip("/' "))
                card_dict = {"store": store_name, "store_id": store_id, "name": name, "sku":sku, "set": set, "col_number": col_number, "lang": lang, "bullshit": bullshit }
                    
                # card_dict["set"] = set
                # card_dict["col_number"] = col_number
                # card_dict["bullshit"] = bullshit
                # card_dict["lang"] = lang

                condition_foil = card['data-varianttitle']
                    
                if 'Foil' in condition_foil:
                    card_dict["foil"] = True
                    card_dict["condition"] = condition_dict[condition_foil.replace('Foil','').strip()]
                else:
                    card_dict["foil"] = False
                    card_dict["condition"] = condition_dict[condition_foil.strip()]
                    
                    
                card_dict["price"] = card['data-variantprice']
                card_dict["available"] = card['data-variantavailable'] == 'true'
                card_dict["quantity"] = card['data-variantqty']
                card_dict["store_link"] = store_link


                cardlist.append(card_dict)
      

    if out_of_stock: #Only if entire page of cards is out of stock
        print("out of stock")
        return cardlist,None  #Stops going through products once out of stock
    

    pagination = soup.find("ol",class_="pagination")
    # print(pagination)
    if pagination == None: # There is only one page
        next_page_url = None
    else:
        next_page = pagination.find_all("li")[-1]
        if next_page.has_attr('class'): #This is the last page
            next_page_url = None
        else:
            next_page_url = base_url + next_page.a['href']
    return cardlist,next_page_url

def template_scraper(url, base_url, store_name):
    out = []
    while url != None:
        cardlist,url = template_scrape_page(url, base_url, store_name)
        out.extend(cardlist)
        # print(len(mtgasia_cardlist))
        time.sleep(0.1)

    return out

def gameshaven_scrape_page(url):
    return template_scrape_page(url, "https://www.gameshaventcg.com/", "Games Haven" )

def greyogregames_scrape_page(url):
    return template_scrape_page(url, "https://www.greyogregames.com/", "Grey Ogre Games" )

def hideout_scrape_page(url):
    return template_scrape_page(url, "https://hideoutcg.com/", "Hideout" )





def gameshaven_scraper(url):
    return template_scraper(url, "https://www.gameshaventcg.com/", "Games Haven" )


# cardlist,url =template_scrape_page('https://www.gameshaventcg.com/search?page=1&q=%2Acultivate%2A',  "https://www.gameshaventcg.com/", "Games Haven" )
# print(cardlist)

def greyogregames_scraper(url):
    return template_scraper(url, "https://www.greyogregames.com/", "Grey Ogre Games" )

# cardlist,url =template_scrape_page('https://www.greyogregames.com/search?q=*rhystic+study*',  "https://www.greyogregames.com/", "Grey Ogre Games" )
# cardlist = greyogregames_scraper("https://www.greyogregames.com/search?page=1&q=%2Acultivate%2A")
# print(cardlist)

# url = "https://www.greyogregames.com/search?page=1&q=%2Acultivate%2A"
# greyogregames_cardlist = greyogregames_scraper(url)
# print(greyogregames_cardlist)

def hideout_scraper(url):
    return template_scraper(url, "https://hideoutcg.com/", "Hideout" )

# def manapro_scraper(url):
#     return template_scraper(url, 'https://sg-manapro.com/', "Mana Pro" )


# cardlist = gameshaven_scraper("https://www.gameshaventcg.com/search?page=1&q=%2Acultivate%20fallouit%2A")
# print(cardlist)