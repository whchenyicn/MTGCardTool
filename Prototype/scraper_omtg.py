from bs4 import BeautifulSoup
import urllib.request
import json


def onemtg_scrape_page(url):
    print(url)
    req = urllib.request.Request(url, data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }    )

    page = urllib.request.urlopen(req)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    product_list = soup.find("div", class_ = ["list-view-items", "products-display"]).find_all(attrs={"data-product-variants": True})
    # print(product_list)

    cardlist = []
    for card in product_list:
        card_dict = json.loads(card["data-product-variants"])
        cardlist.extend(card_dict)

    # print(cardlist)


    next_page = soup.find("div", class_ = "pag_next").find("a") #next_page = None if there is no next page
    
    if next_page != None:
        next_page_url = 'https://onemtg.com.sg' + next_page['href']
    else:
        next_page_url = None   
 
    return cardlist,next_page_url




def onemtg_scraper(url):
    mtgasia_cardlist = []
    while url != None:
        cardlist,url = onemtg_scrape_page(url)
        mtgasia_cardlist.extend(cardlist)
        # print(len(mtgasia_cardlist))

    return mtgasia_cardlist

url = "https://onemtg.com.sg/search?type=product&options%5Bprefix%5D=last&q=cultivate"

# mtgasia_cardlist, url = mtgasia_scrape_page(url)
# onemtg_cardlist = onemtg_scraper(url)
