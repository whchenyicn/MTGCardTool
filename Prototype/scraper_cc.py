from bs4 import BeautifulSoup
import urllib.request
import json
import webpixel_scraper


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

    product_list = soup.find_all("div", class_ ="product Norm")
    for product in product_list:
        buy_wrapper = product.find("div", class_ = "buyWrapper")
        # img = product.find("img")["src"].replace("_large","")
        link = product.find("div",class_ = "view").find("a")["href"].split("?")[0]

        sku = link_to_sku[link]
        # print(img)

        variants = []
        if buy_wrapper != None:
            for div in buy_wrapper.find_all("div", class_ ="addNow single"):
                variant = div["onclick"][10:-1].replace("'","").replace("\"","").split(",")
                variant.append(div.find("p").get_text())
                variants.append(variant)

        # print(variants)
        # print(sku)
        cardlist.append({"sku": sku, "variants": variants})

    # print(cardlist)

    pagination = soup.find("div", id = "pagination" )
    next_page = pagination.find_all("a")[-1]

    if len(next_page["class"]) == 2:
        next_page_url = "https://cardscitadel.com/" + next_page["href"]
    else:
        next_page_url = None
    
    return cardlist,next_page_url



def cardcitadel_scraper(url):
    cardcitadel_cardlist = []
    while url != None:
        cardlist,url = cardcitadel_scrape_page(url)
        cardcitadel_cardlist.extend(cardlist)

    return cardcitadel_cardlist

last_page_url = "https://cardscitadel.com/search?page=8&q=%2Acultivate%2A"

# cardlist = cardcitadel_scraper("https://cardscitadel.com/search?q=*cultivate*")
# print(cardlist)
# cardcitadel_scrape_page(last_page_url)
