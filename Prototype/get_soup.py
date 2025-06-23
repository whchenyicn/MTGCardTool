from bs4 import BeautifulSoup
import urllib.request
import requests



# http_proxy  = "http://40.76.69.94:8080"
# https_proxy = "http://40.76.69.94:8080"

ip = "27.69.244.202"

port = "4008"

http_proxy = "http://" + ip + ":" + port
https_proxy = "https://" + ip + ":" + port

proxies = { 
                "http"  : http_proxy, 
                "https" : https_proxy, 
                }

headers = {
            'User-Agent' : 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341'
        }
    # headers={
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    # } 

def get_soup_proxy(url):
    response = requests.post(url, headers = headers, proxies=proxies)
    # print(response.text)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def get_soup(url):
    req = urllib.request.Request(url, data=None, 
    headers= headers
    )
    page = urllib.request.urlopen(req)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup

url = 'https://www.gameshaventcg.com/search?page=1&q=%2Acultivate%2A'
# url = "http://www.youtube.com/"


# get_soup_proxy(url)