from bs4 import BeautifulSoup
import urllib.request
import json
import webpixel_scraper
import time



def hideout_scrape_page(url):
    print(url)
    cardlist = []
    

    req = urllib.request.Request(url, data=None, 

    headers = {
        'User-Agent' : 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341'
    }
    
    )
    page = urllib.request.urlopen(req)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    id_to_sku = webpixel_scraper.get_id_dict(soup)
    # print(id_to_sku)
    product_list = soup.find_all("div", **{"class_" :"productCard__card", "data-producttype" : "MTG Single"} )
    for product in product_list:
        
        productCard_lower = product.find('div',class_="productCard__lower")
        name = productCard_lower.find('p',class_="productCard__title").get_text().strip()
        set = productCard_lower.find('p',class_="productCard__setName").get_text()
        
        available_cards = productCard_lower.find("ul", class_= "productChip__grid").find_all("li")
        sku = None
        for card in available_cards:
            # if card['data-variantavailable'] == 'true':
            if sku == None:
                id = card["onclick"][14:-1].split(',')[1].strip("/' ")
                sku = id_to_sku[id]
            if True:
                quantity = card['data-variantqty']
                price = card['data-variantprice']
                condition_foil = card['data-varianttitle']
                
                if 'Foil' in condition_foil:
                    foil = True
                    condition = condition_foil.replace('Foil','').strip()
                else:
                    foil = False
                    condition = condition_foil.strip()
                    
                cardlist.append([sku,name,set,condition,foil,price,quantity])
                # print(cardlist[-1])
      

    next_page = soup.find("ol", class_ = "pagination").contents[-1].find("a") #next_page = None if there is no next page

    if next_page != None:
        next_page_url = 'https://hideoutcg.com/' + next_page['href']
    else:
        next_page_url = None   
    return cardlist,next_page_url



def hideout_scraper(url):
    hideout_cardlist = []
    while url != None:
        cardlist,url = hideout_scrape_page(url)
        hideout_cardlist.extend(cardlist)
    time.sleep(0.1)

    return hideout_cardlist



url = "https://hideoutcg.com/search?page=1&q=%2Acultivate%2A"
# hideout_cardlist = hideout_scraper(url)
# print(hideout_cardlist)


