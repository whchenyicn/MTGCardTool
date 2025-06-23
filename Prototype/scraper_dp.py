from bs4 import BeautifulSoup
import urllib.request
import json
import time


def duellerspoint_scrape_page(url):
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

    product_list = soup.find("tbody").find_all("tr")
    for product in product_list:
        card_dict = {}
        td_list = product.find_all("td")
        card_dict["href"] = td_list[1].find("a")["href"]
        card_dict["name"] = td_list[1].find("a").text
        card_dict["set"]  = td_list[2].find("strong").text

        for p in td_list[3].find_all("p"):
            card_dict[p.find("span").text[0:-3]] = p.find("strong").text
        
        stock = td_list[4].find("label").text
        if stock == "Out of Stock":
            card_dict["quantity"]  = 0
        else:
            card_dict["quantity"]  = int(stock[:-5])

        card_dict["price"]  = int(td_list[5].find("span").text[2:].replace(".",""))

        cardlist.append(card_dict)

    next_page = soup.find("a", rel = "next")
    if next_page == None:
        next_page_url = None
    else:
        next_page_url = "https://www.duellerspoint.com/" + next_page["href"]
    
    return cardlist, next_page_url

def duellerspoint_scraper(url):
    duellerspoint_cardlist = []
    while url != None:
        cardlist,url = duellerspoint_scrape_page(url)
        duellerspoint_cardlist.extend(cardlist)

    return duellerspoint_cardlist



# cardlist = duellerspoint_scraper("https://www.duellerspoint.com/products/search?utf8=%E2%9C%93&search_text=cultivate")
# print(cardlist)