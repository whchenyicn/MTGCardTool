from bs4 import BeautifulSoup
import urllib.request
import json


#url = 'https://www.greyogregames.com/search?q=*rhystic+study*'
#url = 'https://www.greyogregames.com/search?q=*kogla*'
#url = 'https://www.greyogregames.com/collections/mtg-singles-all-products'

def greyogregames_scrape_page(url):
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




def greyogregames_scraper(url):
    greyogregames_cardlist = []
    while url != None:
        cardlist,url = greyogregames_scrape_page(url)
        greyogregames_cardlist.extend(cardlist)

    return greyogregames_cardlist




# greyogregames_cardlist = greyogregames_scraper(url)
# write_to_file("greyogregames_cardlist.csv",greyogregames_cardlist)
# print(greyogregames_cardlist)

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
