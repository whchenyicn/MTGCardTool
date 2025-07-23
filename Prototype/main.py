from bs4 import BeautifulSoup
import urllib.request
from urllib.request import urlopen
import urllib
import re
import csv
import json
import time
import sys
import traceback

#local imports
# import scraper_gog as scraper_gog
import scraper_ah
import scraper_ml
import scraper_cc
import scraper_dp
import scraper_multi
import scraper_multi2

import scraper_multi_search
import api_testing


def write_to_csv_file(filename,nestedlist):
    with open(filename,'w',encoding="utf-8", newline='') as f:
        csv.dump(nestedlist, f)
        # csv_writer = csv.writer(f)
        # for listing in nestedlist:
        #     csv_writer.writerow(listing)
            # print(listing)

def write_to_json_file(filename,dictlist):
    with open(filename,'w',encoding="utf-8", newline='') as f:
        json.dump(dictlist, f, indent=4 )
        # for listing in dictlist:
        #     json_object = json.dumps(listing, indent=4)
        #     f.write(json_object)
            
            # print(listing)

def scrape_to_file(url ,scraper, filename):
    cardlist = scraper(url)
    if type(cardlist[0]) == type([0]):
        write_to_csv_file(filename + ".csv" ,cardlist)
    else:
        write_to_json_file(filename + ".json" ,cardlist)

        
# scrape_to_file('https://agorahobby.com/store/search?category=mtg&searchfield=lightning', scraper_ah.agorahobby_scraper, "agorahobby_lightning")

# scrape_to_file('https://www.greyogregames.com/search?page=1&q=%2Acultivate%2A' , scraper_multi2.greyogregames_scraper, "greyogregames_cultivate")
# scrape_to_file('https://www.greyogregames.com/search?q=*lightning*' , scraper_multi2.greyogregames_scraper, "greyogregames_lightning")
# scrape_to_file('https://www.gameshaventcg.com/search?page=1&q=%2Acultivate%2A', scraper_multi2.gameshaven_scraper, "gameshaven_cultivatate")
# scrape_to_file("https://hideoutcg.com/search?page=1&q=%2Acultivate%2A", scraper_multi2.hideout_scraper, "hideout_cultivate")


# scrape_to_file('https://sg-manapro.com/search?type=product&options%5Bprefix%5D=last&q=barone', scraper_multi.manapro_scraper, "manapro_barone")
# scrape_to_file("https://onemtg.com.sg/search?type=product&options%5Bprefix%5D=last&q=cultivate", scraper_multi.onemtg_scraper , "onemtg_cultivate" )
# scrape_to_file("https://www.mtg-asia.com/search?options%5Bprefix%5D=last&page=1&q=cultivate&type=product", scraper_multi.mtgasia_scraper , "mtgasia_cultivate" )
# scrape_to_file("https://card-affinity.com/search?type=product&options%5Bprefix%5D=last&q=cultivate", scraper_multi.cardaffinity_scraper , "cardaffinity_cultivate" )
# scrape_to_file("https://www.cardboardcrackgames.com/search?type=product&options%5Bprefix%5D=last&q=cultivate", scraper_multi.cardboardcrackgames_scraper , "cardboardcrackgames_cultivate" )
# scrape_to_file("https://www.flagshipgames.sg/search?type=product&options%5Bprefix%5D=last&q=cultivate", scraper_multi.flagshipgames_scraper , "flagshipgames_cultivate" )


# scrape_to_file("https://cardscitadel.com/search?q=*cultivate*", scraper_cc.cardcitadel_scraper , "cardcitadel_cultivate" )

# scrape_to_file("https://www.duellerspoint.com/products/search?utf8=%E2%9C%93&search_text=cultivate", scraper_dp.duellerspoint_scraper , "duellerspoint_cultivate")




# scrape_to_file('https://sg-manapro.com/collections/jumpstart-2022', scraper_mp.manapro_scraper, "manapro_jumpstart") #Not working cus something


# scrape_to_file("https://www.moxandlotus.sg/products?title=lightning", scraper_ml.moxandlotus_scraper, "moxandlotus_lightning")
#STILL NOT WORKING




def get_all_scraper(page_scraper, url_list, current_url = None ): #For searching multiple pages on the same website
    if current_url == None:
        current_url = 0
        def next_scraper():
            next_scraper.url = url_list[current_url]
            return get_all_scraper(page_scraper, url_list, current_url)
        
        return next_scraper
    else:
        print("running all_scraper")
        cardlist,url_list[current_url] = page_scraper(url_list[current_url])

        if url_list[current_url] == None:
            current_url += 1

            if current_url >= len(url_list): #finished scraping
                print("finished scraping current website")
                return cardlist, None
    
        def next_scraper():
            next_scraper.url = url_list[current_url]
            return get_all_scraper(page_scraper, url_list, current_url)

        return cardlist, next_scraper

def get_asc_desc_scraper(first_url, second_url, page_scraper):
    
    def asc_scraper():
        cardlist, next_url = page_scraper(asc_scraper.url )
        if next_url == None:
            desc_scraper.stop_id = cardlist[-1]["store_id"]
            return cardlist, desc_scraper
        else:
            asc_scraper.url = next_url
            return cardlist, asc_scraper
        

    asc_scraper.url = first_url
    
    def desc_scraper():
        cardlist, next_url = page_scraper(desc_scraper.url )

        for i in range(len(cardlist)):
            if cardlist[i]["store_id"] == desc_scraper.stop_id:
                cardlist = cardlist[:i]
                return cardlist, None
        

        if next_url == None:
            return cardlist, None
        else:
            desc_scraper.url = next_url
            return cardlist, desc_scraper
        


    desc_scraper.url = second_url

    return asc_scraper   



with open("handle_list1.csv", "r" ) as f:
    handle_list1 = f.read().splitlines()
handle_list_short = handle_list1[4:10]

with open("handle_list2.csv", "r" ) as f:
    handle_list2 = f.read().splitlines()

# print(["https://www.mtg-asia.com/collections/non-foil/" + handle for handle in handle_list[0:10]])
multi_all_short = [[get_all_scraper(scraper_multi.mtgasia_scrape_page, ["https://www.mtg-asia.com/collections/non-foil/" + handle for handle in handle_list_short]) , "mtgasia_all" ], 
                   [get_all_scraper(scraper_multi.onemtg_scrape_page, ["https://onemtg.com.sg/collections/mtg-singles-all-products/" + handle for handle in handle_list_short]) , "onemtg_all" ],
                   [get_all_scraper(scraper_multi_search.cardaffinity_scrape_page, ["https://card-affinity.com/search?type=product&options%5Bprefix%5D=last&q=" + handle for handle in handle_list2[:len(handle_list_short)] ]) , "cardaffinity_all" ],
                   [get_all_scraper(scraper_multi_search.flagshipgames_scrape_page, ["https://www.flagshipgames.sg/search?type=product&options%5Bprefix%5D=last&q=" + handle for handle in handle_list2[:len(handle_list_short)]]) , "flagshipgames_all" ],
                   [get_all_scraper(scraper_multi2.greyogregames_scrape_page, ["https://www.greyogregames.com/collections/mtg-singles-all-products/" + handle for handle in handle_list_short]) , "greyogregames_all" ],
                   [get_all_scraper(scraper_multi2.hideout_scrape_page, ["https://hideoutcg.com/collections/mtg-singles/" + handle for handle in handle_list_short]) , "hideout_all" ]
                   ]

multi_all_sets = [[get_all_scraper(scraper_multi.mtgasia_scrape_page, ["https://www.mtg-asia.com/collections/non-foil/" + handle for handle in handle_list1]) , "mtgasia_all" ], 
                   [get_all_scraper(scraper_multi.onemtg_scrape_page, ["https://onemtg.com.sg/collections/mtg-singles-all-products/" + handle for handle in handle_list1]) , "onemtg_all" ],
                   [get_all_scraper(scraper_multi_search.cardaffinity_scrape_page, ["https://card-affinity.com/search?type=product&options%5Bprefix%5D=last&q=" + handle for handle in handle_list2]) , "cardaffinity_all" ],
                   [get_all_scraper(scraper_multi_search.flagshipgames_scrape_page, ["https://www.flagshipgames.sg/search?type=product&options%5Bprefix%5D=last&q=" + handle for handle in handle_list2]) , "flagshipgames_all" ],
                   [get_all_scraper(scraper_multi2.greyogregames_scrape_page, ["https://www.greyogregames.com/collections/mtg-singles-all-products/" + handle for handle in handle_list1]) , "greyogregames_all" ],
                   [get_all_scraper(scraper_multi2.hideout_scrape_page, ["https://hideoutcg.com/collections/mtg-singles/" + handle for handle in handle_list1]) , "hideout_all" ]
                   ]

multi_all_the_list = [[get_all_scraper(scraper_multi.mtgasia_scrape_page, ["https://www.mtg-asia.com/collections/non-foil/" + "the-list"]) , "mtgasia_plst" ], 
                   [get_all_scraper(scraper_multi.onemtg_scrape_page, ["https://onemtg.com.sg/collections/mtg-singles-all-products/" + "the-list"]) , "onemtg_plst" ],
                   [get_all_scraper(scraper_multi_search.cardaffinity_scrape_page, ["https://card-affinity.com/search?type=product&options%5Bprefix%5D=last&q=" + "the-list"]) , "cardaffinity_plst" ],
                   [get_all_scraper(scraper_multi_search.flagshipgames_scrape_page, ["https://www.flagshipgames.sg/search?type=product&options%5Bprefix%5D=last&q=" + "the-list"]) , "flagshipgames_plst" ],
                   [get_all_scraper(scraper_multi2.greyogregames_scrape_page, ["https://www.greyogregames.com/collections/mtg-singles-all-products/" + "the-list"]) , "greyogregames_plst" ],
                   [get_all_scraper(scraper_multi2.hideout_scrape_page, ["https://hideoutcg.com/collections/mtg-singles/" + "the-list"]) , "hideout_plst" ]
                   ]


# multi_asc_dsc = [[scraper_cc.cardcitadel_get_all_scraper() , "cardcitadel_all" ],
#                  [scraper_multi.manapro_get_all_scraper() , "manapro_all" ] 
#                  ]

multi_asc_dsc = [[get_asc_desc_scraper("https://cardscitadel.com/collections/mtg-singles-instock?sort_by=title-ascending", 
                                       "https://cardscitadel.com/collections/mtg-singles-instock?sort_by=title-descending",  
                                       scraper_cc.cardcitadel_scrape_page ) , "cardcitadel_all" ],
                 [get_asc_desc_scraper("https://sg-manapro.com/collections/mtg-singles-all-products?page=1", 
                                       "https://sg-manapro.com/collections/mtg-singles-all-products?sort_by=title-descending",  
                                       scraper_multi.manapro_scrape_page ) , "manapro_all" ]
                 ]

multi_whole = [ 
    # [get_all_scraper(scraper_dp.duellerspoint_scrape_page, ["https://www.duellerspoint.com/products/search?utf8=%E2%9C%93&search_text=&foil_type=&button=&category_ids%5B%5D=10&stock_type=available&card+type_ids%5B%5D=&color_ids%5B%5D=&condition_ids%5B%5D=&edition_ids%5B%5D=&rarity_ids%5B%5D="]
    #                               ) , "duellerspoint_all" ],
            
    [get_all_scraper(scraper_multi.cardboardcrackgames_scrape_page, ["https://www.cardboardcrackgames.com/collections/mtg-singles"]) , "cardboardcrackgames_all" ],
            ]

multi_all = multi_all_sets + multi_asc_dsc + multi_whole
# print(multi_all)

def multi_all_scraper(multi, limit = None, database = False):  #For searching multiple pages on multiple websites
    
    count = 0
    update_every = 500
    update_count = update_every
    done = 0
    if database:
        db_conn = api_testing.get_db_conn()
    else:
        out = [[] for x in range(len(multi)) ]
    error = [{"store": x[1], "error":None, "traceback": None , "last_url":None, "finish_running": False, "length":0 } for x in multi ]
    write_to_json_file("errors.json", error)
    prev_time = time.time()

    while done < len(multi):
        print("scraping next set")
        for i in range(len(multi)):
            if multi[i][0] == None:
                continue
            else:
                try:
                    cardlist,next_scraper = multi[i][0]()
                    print(len(cardlist))
                    error[i]["length"] += len(cardlist)
                    if database:
                        api_testing.upload_to_database(cardlist,db_conn)
                    else:
                        out[i].extend(cardlist)
                    multi[i][0] = next_scraper

                    if next_scraper == None:
                        if not database:
                            write_to_json_file(multi[i][1] + ".json" ,out[i] )
                        done += 1
                        error[i]["finish_running"] = True


                except Exception as ex:
                    ex_type, ex_value, ex_traceback = sys.exc_info()
                    # Extract unformatter stack traces as tuples
                    trace_back = traceback.extract_tb(ex_traceback)
                    # Format stacktrace
                    stack_trace = list()
                    for trace in trace_back:
                        stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

                    # print("ERROR", type(ex) )
                    # print("repr",str(repr(ex)) )
                    error[i]["error"] = str(ex_type.__name__)
                    error[i]["exception_message"] = str(ex_value)
                    error[i]["traceback"] = stack_trace
                    error[i]["last_url"] = multi[i][0].url
                    print(error[i])
                    multi[i][0] = None
                    write_to_json_file("errors.json", error)
                    write_to_json_file(multi[i][1] + ".json" ,out[i] )
                    
                    
                    done += 1
        
        time_taken = time.time() - prev_time
        # print("time taken:", time_taken)

        if time.time() - prev_time < 1:
            time.sleep(1- time_taken)
            # print("sleeping for ", 1 - time_taken)
        prev_time = time.time()

        count += 1
        if limit != None:
            if count >= limit:
                for d in error:
                    d["finish_running"] = True
                break
        
        #Updates database every 100 pages
        if not database:
            if count >= update_count:
                for i in range(len(out)):
                    if multi[i][0] != None:
                        write_to_json_file(multi[i][1] + ".json" ,out[i] )
                update_count = update_count+update_every

                
                
    if database:
        db_conn.close()
    else:
        for i in range(len(out)):
            write_to_json_file(multi[i][1] + ".json" ,out[i] )
            error[i]["length"] = len(out[i])

    
    write_to_json_file("errors.json", error)
            
# multi_all_scraper(multi_all_short[:2], limit=100, database=True)

# mtgasia_test = [ [get_all_scraper(scraper_multi.mtgasia_scrape_page, ["https://www.mtg-asia.com/collections/non-foil/dominaria-tokens"]) , "mtgasia_tdom" ] ]

# multi_all_scraper(mtgasia_test, database=True)


# scraper_multi.mtgasia_scrape_page("https://www.mtg-asia.com/collections/non-foil/15th-anniversary")



# scraper_multi.mtgasia_scrape_page("https://www.mtg-asia.com/collections/non-foil/aether-revolt")




















# def multi_scraper(multi, handle = None):
#     if handle != None:
#         for site in multi:
#             site[0] = site[0] + handle

#     done = 0
#     out = [[] for x in range(len(multi)) ]

#     while done < len(out):
#         for i in range(len(multi)):
#             time.sleep(1/len(multi))
#             if multi[i][0] == None:
#                 continue
#             else:
#                 try:
#                     cardlist,url = multi[i][1](multi[i][0])
#                     out[i].extend(cardlist)
#                     multi[i][0] = url

#                     if url == None:
#                         done += 1
#                 except:
#                     multi[i][0] = None
#                     done += 1
                
                
    
#     for i in range(len(out)):
#         write_to_json_file(multi[i][2] + ".json" ,out[i] )

                


# multi_search = [ ["https://cardscitadel.com/search?q=*cultivate*", scraper_cc.cardcitadel_scrape_page , "cardcitadel_cultivate"] ,
#           ['https://sg-manapro.com/search?type=product&options%5Bprefix%5D=last&q=barone', scraper_multi_search.manapro_scrape_page, "manapro_barone"] ,
#           ["https://onemtg.com.sg/search?type=product&options%5Bprefix%5D=last&q=cultivate", scraper_multi_search.onemtg_scrape_page , "onemtg_cultivate"] ,
#           ["https://www.mtg-asia.com/search?options%5Bprefix%5D=last&page=1&q=cultivate&type=product", scraper_multi_search.mtgasia_scrape_page , "mtgasia_cultivate" ]
#         ]




# mult_all = [
#             ["https://cardscitadel.com/collections/mtg-singles-instock", scraper_cc.cardcitadel_scrape_page , "cardcitadel_all"] , 
#             ["https://www.mtg-asia.com/collections/non-foil", scraper_multi.mtgasia_scrape_page, "mtgasia_all" ] ,
#             # ["https://card-affinity.com/collections/all", scraper_multi.cardaffinity_scrape_page, "cardaffinity_all" ] ,
#             ["https://www.cardboardcrackgames.com/collections/mtg-singles", scraper_multi.cardboardcrackgames_scrape_page, "cardboardcrackgames_all" ] ,
#             ["https://sg-manapro.com/collections/mtg-singles-all-products", scraper_multi.manapro_scrape_page, "manapro_all" ] ,
#             ["https://onemtg.com.sg/collections/mtg-singles-all-products", scraper_multi.onemtg_scrape_page, "onemtg_all" ] 
#           ]


# multi_scraper(mult_all)
