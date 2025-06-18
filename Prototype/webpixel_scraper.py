from bs4 import BeautifulSoup
import json

def get_json(soup):
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
    return cardlist

def get_id_dict(soup):
    cardlist = get_json(soup)

    id_dict = {}
    for card in cardlist:
        id = card["id"]
        sku = card["sku"]
        id_dict[id] = sku

    return id_dict

def get_img_dict(soup):
    cardlist = get_json(soup)

    img_dict = {}
    for card in cardlist:
        img = card["image"]["src"]
        sku = card["sku"]
        img_dict[img] = sku

    return img_dict

def get_link_dict(soup):
    cardlist = get_json(soup)

    link_dict = {}
    for card in cardlist:
        link = card["product"]["url"].split("?")[0]
        sku = card["sku"]
        link_dict[link] = sku

    return link_dict