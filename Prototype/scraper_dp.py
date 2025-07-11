from bs4 import BeautifulSoup
import urllib.request
import json
import time

condition_dict = {"Near Mint": 1 , "Lightly Played": 2, "Moderately Played": 3, "Heavily Played": 4, "Damaged": 5 }

def duellerspoint_scrape_page(url):
    print(url)
    cardlist = []
    out_of_stock = False

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
        td_list = product.find_all("td")
        stock = td_list[4].find("label").text
        if stock == "Out of Stock":
            out_of_stock = True
            break


        card_dict = {"store": "Dueller's Point", "store_id": None}
        card_dict["set"]  = td_list[2].find("strong").text
        name_list = td_list[1].find("a").text.split("(")
        card_dict["col_number"] = name_list.pop(0).strip()
        card_dict["foil"] = td_list[1].find("span") != None
        if card_dict["foil"]:
            foil_str = name_list.pop()
            if foil_str != "Foil)":
                print(foil_str)

        temp_dict = {}
        for p in td_list[3].find_all("p"):
            temp_dict[p.find("span").text[0:-3]] = p.find("strong").text

        card_dict["condition"] = condition_dict[temp_dict["Condition"]]
        
        if len(name_list) == 0:
            card_dict["lang"] = "en"
            card_dict["bullshit"] = None
        else:
            bullshit = ",".join(name_list)
            if "jp " in bullshit or "japanese" in bullshit:
                card_dict["lang"] = "jp"
            else:
                card_dict["lang"] = "en"
            card_dict["bullshit"] = bullshit

        card_dict["price"]  = int(td_list[5].find("span").text[2:].replace(".",""))

        card_dict["available"] = True
        card_dict["quantity"]  = int(stock[:-5])

        
        card_dict["store_link"] = "https://www.duellerspoint.com/" + td_list[1].find("a")["href"]

        cardlist.append(card_dict)

    next_page = soup.find("a", rel = "next")
    if next_page == None or out_of_stock:
        next_page_url = None
    else:
        next_page_url = "https://www.duellerspoint.com/" + next_page["href"]
    
    return cardlist, next_page_url

def duellerspoint_scraper(url):
    duellerspoint_cardlist = []
    while url != None:
        cardlist,url = duellerspoint_scrape_page(url)
        duellerspoint_cardlist.extend(cardlist)
        time.sleep(0.1)

    return duellerspoint_cardlist



# cardlist = duellerspoint_scraper("https://www.duellerspoint.com/products/search?utf8=%E2%9C%93&search_text=cultivate")
# print(cardlist)