from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def moxandlotus_scrape_page(driver, cardlist):
    
# selenium waits for page to be loaded
    strong_product = driver.find_element(By.TAG_NAME,"strong")

    first_page = False
    if strong_product.text == "Product found":
        first_page = True
    

    # time.sleep(5)
    wait = WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "strong"), "Products")
        )
    strong_product = driver.find_element(By.TAG_NAME,"strong")
    print(strong_product.text)

# wait for page to change
    if not first_page:
        print("not first page")
        first_card = driver.find_element(By.TAG_NAME, "tr")
        a = first_card.find_elements(By.TAG_NAME, "a")[1]
        a = first_card.find_element(By.CLASS_NAME,"title")
        link = a.get_attribute("href")
        print(link)


        print(first_card.text)
        wait = WebDriverWait(first_card, 10).until(
            EC.none_of(
                EC.text_to_be_present_in_element_attribute((By.CLASS_NAME,"title"), "href", link)
            )
        )


#Open page in beautiful soup cus its easier to scrape
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    row_card = soup.find("div", class_ = "row card")

    cards = row_card.find("table").tbody.contents
    print(len(cards))
    for card in cards:
        # print(card.text)
        carddict = {}
        img_source = card.find("img")["data-src"]
        carddict["sku"] = img_source[38:-4]
        carddict["foil"] = card.find("div", class_ = "foil-filter") != None

        # print(carddict["sku"], carddict["foil"])
        variants = {}
        td_list = card.find_all("td")
        price_list = td_list[4].contents

        quantity_list = td_list[5].contents
        conditions = ["NM", "EX", "VG", "L"]

        for i in range(4):
            condition = conditions[i]
            price = price_list[i].text.strip()

            if len(quantity_list[i]["class"]) == 2:
                quantity = 0
            else:
                if quantity_list[i].p.span.text == "Out of Stock":
                    quantity = 0
                else:
                    quantity = len(quantity_list[i].find("div", class_ = "popper").find_all("button")) - 1
            # print(condition, price, quantity)

            variant = {}
            variant["price"] = price
            variant["quantity"] = quantity
            variants[condition] = variant

        carddict["variants"] = variants
        cardlist.append(carddict)

#Checks if theres a next page
    pagination = soup.find("ul", class_ ="pagination flex-wrap")
    pages = pagination.find_all("li")
    print(pages[-1]["class"])
    if pages[-1]["class"][-1] == "disabled": #If theres no xext page
        print("last page")
        driver.quit()
        return None, cardlist
    else: #If there is a next page, clicks next page button
        print("next page")
        sel_pagination = driver.find_element(By.CLASS_NAME, "pagination")
        sel_pages = sel_pagination.find_elements(By.TAG_NAME, "li")
        sel_next_button = sel_pages[-1]
        print(sel_next_button.text)
        sel_next_button.find_element(By.TAG_NAME,"a").click()
        return driver, cardlist


def moxandlotus_scraper(url):
    driver = webdriver.Chrome()
    driver.get(url)
    cardlist = []

    #Click list view in selenium
    header = driver.find_elements(By.CLASS_NAME,"mb-3")[1]
    button_grp = header.find_element(By.CLASS_NAME,"btn-group")
    list_button = button_grp.find_elements(By.TAG_NAME,"a")[1]
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(list_button))
    element = WebDriverWait(driver, 10).until(
        EC.none_of(
            EC.presence_of_element_located((By.CLASS_NAME, "swal2-container"))
        )
        )
    
    # print(element.text)
    list_button.click()

    

    #Click All variations in selenium
    wait = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "article"))
        )
    aside = driver.find_element(By.TAG_NAME, "aside")
    variation_filter = aside.find_elements(By.TAG_NAME, "article")[2]
    variation_filter.find_element(By.TAG_NAME, "label").click()

    driver, cardlist = moxandlotus_scrape_page(driver, cardlist)

    page = 1
    while driver != None and page <= 10: #Driver == None on the last page
        driver, cardlist = moxandlotus_scrape_page(driver, cardlist)
        page += 1

    print(len(cardlist))



# moxandlotus_scraper("https://www.moxandlotus.sg/products?title=cultivate")
moxandlotus_scraper("https://www.moxandlotus.sg/products?title=lightning")
# moxandlotus_scraper("https://moxandlotus.sg/products?title=golden%20throne")