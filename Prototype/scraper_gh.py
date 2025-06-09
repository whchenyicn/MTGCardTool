from bs4 import BeautifulSoup
import urllib.request
import json

def gameshaven_scrape_page(url):
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




def old_gameshaven_scrape_page(url):
    print(url)

    req = urllib.request.Request(url, data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }    )
    page = urllib.request.urlopen(req)
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
