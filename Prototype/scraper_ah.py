from bs4 import BeautifulSoup
import urllib.request
import json
import re

def agorahobby_scrape_page(url):
    print(url)
    cardlist = []

    req = urllib.request.Request(url, data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }    )

    page = urllib.request.urlopen(req)
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

