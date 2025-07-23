import requests
import json
import os
from psycopg2 import pool
import time

# url = "https://api.scryfall.com/cards/xln/96"
# response = requests.get(url)
# data = response.json()
# print(data)

def get_allcards_db():
    # Get the connection string from the environment variable
    connection_string = "postgresql://neondb_owner:npg_QVwXH1Lz8khP@ep-misty-brook-a8wo0xpx-pooler.eastus2.azure.neon.tech/allCards?sslmode=require&channel_binding=require"
    # Create a connection pool
    connection_pool = pool.SimpleConnectionPool(
        1,  # Minimum number of connections in the pool
        10,  # Maximum number of connections in the pool
        connection_string
    )
    # Get a connection from the pool
    conn = connection_pool.getconn()
    # Create a cursor object
    cur = conn.cursor()
    # Execute SQL commands to retrieve the current time and version from PostgreSQL


    # cur.execute('SELECT NOW();')
    # time = cur.fetchone()[0]
    # cur.execute('SELECT version();')
    # version = cur.fetchone()[0]
    
    
    def close():
        # Close the cursor and return the connection to the pool
        cur.close()
        connection_pool.putconn(conn)
        # Close all connections in the pool
        connection_pool.closeall()
    
    return conn, cur, close

def get_db_conn():
    connection_string = "postgresql://neondb_owner:npg_QVwXH1Lz8khP@ep-misty-brook-a8wo0xpx-pooler.eastus2.azure.neon.tech/allCards?sslmode=require&channel_binding=require"
    connection_pool = pool.SimpleConnectionPool(
        1,  # Minimum number of connections in the pool
        10,  # Maximum number of connections in the pool
        connection_string
    )
    conn = connection_pool.getconn()
    cur = conn.cursor()
    
    def close():
        # Close the cursor and return the connection to the pool
        cur.close()
        connection_pool.putconn(conn)
        # Close all connections in the pool
        connection_pool.closeall()

    get_db_conn.conn = conn
    get_db_conn.cur = cur
    get_db_conn.close = close

    
    return get_db_conn
store_dict = {"MTG Asia": "mtgasia", "One MTG":"onemtg" }



def update_scryfall_table(card, db_conn):
    #Updates store_id in scryfall
    store_name = store_dict[card["store"]]
    db_conn.cur.execute(
        f"""SELECT {store_name}_id FROM scryfall WHERE id = %(scryfall_id)s ;""", card)
    prev_store_id = db_conn.cur.fetchone()[0]
    if prev_store_id == None: #If this is the first of this card from this store
        db_conn.cur.execute(
            f"""UPDATE scryfall 
            SET {store_name}_id = %(store_id)s
            WHERE id = %(scryfall_id)s ;""", card)
        # db_conn.conn.commit()
    
    elif prev_store_id == 0: #store_id = 0 means that this store offers multiple products of this type of card with different conditions or foil
        pass
    elif prev_store_id == card["store_id"]:
        print("yo what the fuck ive seen this card before")
    else: #If store_id currently holds an actual store_id, there is only 1 product of this card being sold
        #changing store id to 0
        db_conn.cur.execute(
            f"""UPDATE scryfall 
            SET {store_name}_id = 0
            WHERE id = %(scryfall_id)s ;""", card)
        # db_conn.conn.commit()



def update_store_table(card, db_conn):
    store_name = store_dict[card["store"]]
    db_conn.cur.execute(f"""UPDATE {store_name} 
                SET price = %(price)s, quantity = %(quantity)s, available = %(available)s
                WHERE store_id = %(store_id)s;""", card )
    # db_conn.conn.commit()


def reset_database(db_conn):
    db_conn.cur.execute(
        """UPDATE scryfall
        SET mtgasia_id = NULL ;""")
    # db_conn.conn.commit()

    db_conn.cur.execute(
        """UPDATE mtgasia
        SET available = false ;""")
    # db_conn.conn.commit()

def upload_to_database(cardlist, db_conn):

    for card in cardlist:
        store_name = store_dict[card["store"]]
        db_conn.cur.execute(
        f"""SELECT scryfall_id store_id FROM {store_name} WHERE store_id = %(store_id)s ;""", card)
        scryfall_id = db_conn.cur.fetchone()

        if scryfall_id == None: #if there are no cards with this id already in store database
            print(f"{card["name"]} not in {store_name} database")


            #Retrieves card information from scryfall API
            scryfall_data = get_card_from_scryfall_api(card)
            if scryfall_data == None:
                continue
            card["scryfall_id"] = scryfall_data["id"]


            db_conn.cur.execute("SELECT COUNT(1) FROM scryfall WHERE id = %(id)s;", scryfall_data)
            result = db_conn.cur.fetchone()
            if result[0] == 0: #if there are no cards with this id already in scryfall database
                print(card["name"],"not in scryfall database, adding")
                

                #Adds card information to scryfall database
                scryfall_data["store_name"] = store_name
                store_id = card["store_id"]

                if "image_uris" in scryfall_data:
                    scryfall_data["image_uri"] = scryfall_data["image_uris"]["small"]
                else:
                    scryfall_data["image_uri"] = scryfall_data["card_faces"][0]["image_uris"]["small"]

                db_conn.cur.execute(f"""INSERT INTO scryfall (id, card_name, set, col_number, lang, set_name, image_uri, {store_name}_id ) 
                VALUES (%(id)s, %(name)s , %(set)s, %(collector_number)s , %(lang)s , %(set_name)s , %(image_uri)s , {store_id} ) ;""" , scryfall_data  )
                db_conn.conn.commit()


            else: #If this card is already in scryfall database
                print(card["name"],"already in scryfall database")
                update_scryfall_table(card, db_conn)

                

            #Adds product entry into store_db
            db_conn.cur.execute(f"""INSERT INTO {store_name} (store_id, scryfall_id, foil, condition, store_link, price, quantity, available ) 
                VALUES ( %(store_id)s,  '{scryfall_data["id"]}' , %(foil)s, %(condition)s , %(store_link)s, %(price)s , %(quantity)s , %(available)s) ;""", card )
            # db_conn.conn.commit()
            print(f"{card["name"]} added to {store_name} database" )


        else:
            print(f"{card["name"]} already in {store_name} database")
            card["scryfall_id"] = scryfall_id[0]


            update_scryfall_table(card, db_conn)
            update_store_table(card, db_conn)

    db_conn.conn.commit()


def batch_upload_database(cardlist, db_conn):
    if len(cardlist) == 0:
        return
    
    print("running batch_upload_database")
    store_name = store_dict[cardlist[0]["store"] ]
    db_conn.cur.execute(f'''CREATE TABLE IF NOT EXISTS "public"."temp_{store_name}" (
                            "store_id" bigint PRIMARY KEY,
                            "price" integer,
                            "quantity" integer);''')
    
    
    
    db_conn.conn.commit()


def batch_upload_database_test():
    with open("mtgasia_tdom.json", "r" ) as f:
        cardlist = json.load(f)
        # print(mtgasia_cardlist)
    
    db_conn = get_db_conn()

    batch_upload_database(cardlist,db_conn )
    db_conn.close()


batch_upload_database_test()




















def mtgasia_test():
    def update_scryfall_table(card):
        #Updates store_id in scryfall
        store_name = store_dict[card["store"]]
        cur.execute(
            f"""SELECT {store_name}_id FROM scryfall WHERE id = %(scryfall_id)s ;""", card)
        prev_store_id = cur.fetchone()[0]
        if prev_store_id == None: #If this is the first of this card from this store
            cur.execute(
                f"""UPDATE scryfall 
                SET {store_name}_id = %(store_id)s
                WHERE id = %(scryfall_id)s ;""", card)
            conn.commit()
        
        elif prev_store_id == 0: #store_id = 0 means that this store offers multiple products of this type of card with different conditions or foil
            pass
        elif prev_store_id == card["store_id"]:
            print("yo what the fuck ive seen this card before")
        else: #If store_id currently holds an actual store_id, there is only 1 product of this card being sold
            cur.execute(
                f"""UPDATE scryfall 
                SET {store_name}_id = 0
                WHERE id = %(scryfall_id)s ;""", card)
            conn.commit()



    def update_store_table(card):
        store_name = store_dict[card["store"]]
        cur.execute(f"""UPDATE {store_name} 
                    SET price = %(price)s, quantity = %(quantity)s, available = %(available)s
                    WHERE store_id = %(store_id)s;""", card )
        conn.commit()


    conn, cur, close = get_allcards_db()


    with open("mtgasia_all.json", "r" ) as f:
        mtgasia_cardlist = json.load(f)
        # print(mtgasia_cardlist)

    cur.execute(
        """UPDATE scryfall
        SET mtgasia_id = NULL ;""")
    conn.commit()

    cur.execute(
        """UPDATE mtgasia
        SET available = false ;""")
    conn.commit()


    mtgasia_cardlist = mtgasia_cardlist[0:5]
    store_dict = {"MTG Asia": "mtgasia" }
    store_name = "mtgasia"
    for card in mtgasia_cardlist:

        cur.execute(
        f"""SELECT scryfall_id store_id FROM {store_name} WHERE store_id = %(store_id)s ;""", card)
        scryfall_id = cur.fetchone()

        if scryfall_id == None: #if there are no cards with this id already in store database
            print(f"{card["name"]} not in {store_name} database")


            #Retrieves card information from scryfall API
            scryfall_data = get_card_from_scryfall_api(card)
            card["scryfall_id"] = scryfall_data["id"]


            cur.execute("SELECT COUNT(1) FROM scryfall WHERE id = %(id)s;", scryfall_data)
            result = cur.fetchone()
            if result[0] == 0: #if there are no cards with this id already in scryfall database
                print(card["name"]," not in scryfall database, adding")
                

                #Adds card information to scryfall database
                scryfall_data["store_name"] = store_name
                store_id = card["store_id"]

                if "image_uris" in scryfall_data:
                    scryfall_data["image_uri"] = scryfall_data["image_uris"]["small"]
                else:
                    scryfall_data["image_uri"] = scryfall_data["card_faces"][0]["image_uris"]["small"]

                cur.execute(f"""INSERT INTO scryfall (id, card_name, set, col_number, lang, set_name, image_uri, {store_name}_id ) 
                VALUES (%(id)s, %(name)s , %(set)s, %(collector_number)s , %(lang)s , %(set_name)s , %(image_uri)s , {store_id} ) ;""" , scryfall_data  )
                conn.commit()


            else:
                print(card["name"]," already in scryfall database")

                update_scryfall_table(card)

                

            #Adds product entry into store_db
            cur.execute(f"""INSERT INTO {store_name} (store_id, scryfall_id, foil, condition, store_link, price, quantity, available ) 
                VALUES ( %(store_id)s,  '{scryfall_data["id"]}' , %(foil)s, %(condition)s , %(store_link)s, %(price)s , %(quantity)s , %(available)s) ;""", card )
            conn.commit()
            print(f"{card["name"]} added to {store_name} database" )


        else:
            print(f"{card["name"]} already in {store_name} database")
            card["scryfall_id"] = scryfall_id[0]


            update_scryfall_table(card)
            update_store_table(card)
    close()


def get_set_dict():
    set_dict = {}
    scryfall_data = requests.get("https://api.scryfall.com/sets").json()["data"]
    for set in scryfall_data:
        set_dict[set["code"] ] = set["code"]
        set_dict[set["name"] ] = set["code"]

    set_dict["list"] = "plst"
    set_dict["plist"] = "plst"
    set_dict["mb1"] = "plst"
    return set_dict

# set_dict = get_set_dict()
# print(set_dict)

def get_card_from_scryfall_api(card):
    if card["set"] in set_dict:
        set_code = set_dict[card["set"] ]
    else:
        print("Error no set code for ", card["set"])
        return None


    if card["col_number"] != None: #Attempts to search using col_number if it exists
        if set_code == "plst" and card["bullshit"] != None:
            list_number = card["bullshit"].split("/")[0]
            if list_number[0] == "0":
                list_number = list_number[1:]
            card["col_number"] = card["col_number"].upper() + "-" + list_number
            
        url = "https://api.scryfall.com/cards/" + set_code + "/" + card["col_number"] + "/" + card["lang"]
        print(url)
        scryfall_data = requests.get(url).json()
        time.sleep(0.1)
        if scryfall_data["object"] == "card":
            print("success!")
            return scryfall_data    
        elif scryfall_data["object"] == "error" and scryfall_data["code"] == "not_found":
            print("card sku not found", url)
        else:
            print("what the hell")
            print(scryfall_data)
        

    #If search fails or if theres no col_number, attempts to search by card name
    if card["foil"]:
        foil = "foil"
    else:
        foil = "nonfoil"
    url = f'https://api.scryfall.com/cards/search?q=unique:prints+set:{set_code}+name:!"{card["name"]}"+lang:{card["lang"]}+is:{foil}'
    print(url)
    scryfall_data = requests.get(url).json()
    if scryfall_data["object"] == "list":
        if scryfall_data["total_cards"] == 1:
            card_data = scryfall_data["data"][0]
            print("success!")
            return card_data
        else:
            print("Error: multiple cards found")
            for card_data in scryfall_data["data"]:
                print(card_data["collector_number"] )
            return scryfall_data["data"][0]
    elif scryfall_data["object"] == "error" and scryfall_data["code"] == "not_found":
        print("Error: no card found")
        return None
    else:
        print("what the hell")
        print(scryfall_data)



# card = {"name": "Cultivate", "col_number": None, "set":"Fallout" , "lang":"es", "foil":False}
# get_card_from_scryfall_api(card)
# card = {"name": "Cultivate", "col_number": "724", "set":"Fallout" , "lang": "en" }
# get_card_from_scryfall_api(card)

def get_card_from_scryfall_api_test():
    mtgasia_plst = "mtgasia_plst.json"
    onemtg_plst = "onemtg_plst.json"

    cardboardcrackgames_all = "cardboardcrackgames_all.json"

    with open(cardboardcrackgames_all, "r" ) as f:
        success = 0
        fail = 0
        cardlist = json.load(f)
        # print(mtgasia_cardlist)
        for card in cardlist:
            scryfall_data = get_card_from_scryfall_api(card)
            # print(scryfall_data)
            if scryfall_data == None:
                fail += 1
            else:
                success += 1
            print("success", success, "fail", fail   )

    print("success", success, "fail", fail)
