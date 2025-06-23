from bs4 import BeautifulSoup
import urllib.request
import json
import webpixel_scraper
import time


#url = 'https://www.greyogregames.com/search?q=*rhystic+study*'
#url = 'https://www.greyogregames.com/search?q=*kogla*'
#url = 'https://www.greyogregames.com/collections/mtg-singles-all-products'

def greyogregames_scrape_page(url):
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
        next_page_url = 'https://www.greyogregames.com/' + next_page['href']
    else:
        next_page_url = None   
    return cardlist,next_page_url



def greyogregames_scraper(url):
    greyogregames_cardlist = []
    while url != None:
        cardlist,url = greyogregames_scrape_page(url)
        greyogregames_cardlist.extend(cardlist)
    time.sleep(0.1)

    return greyogregames_cardlist



# url = "https://www.greyogregames.com/search?page=1&q=%2Alightning%2A"
# greyogregames_cardlist = greyogregames_scraper(url)
# print(greyogregames_cardlist)



# write_to_file("greyogregames_cardlist.csv",greyogregames_cardlist)

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















def webpixels_greyogregames_scrape_page(url):
    print(url)
    req = urllib.request.Request(url, data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }    )

    page = urllib.request.urlopen(req)
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