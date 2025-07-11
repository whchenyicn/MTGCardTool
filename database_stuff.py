import json

import os
from psycopg2 import pool


def get_allcards_cur():
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


    cur.execute('SELECT NOW();')
    time = cur.fetchone()[0]
    cur.execute('SELECT version();')
    version = cur.fetchone()[0]
    return cur

# def close_allcards_cur():
#     # Close the cursor and return the connection to the pool
#     cur.close()
#     connection_pool.putconn(conn)
#     # Close all connections in the pool
#     connection_pool.closeall()



# # Print the results
# print('Current time:', time)
# print('PostgreSQL version:', version)
count = 0
with open("default-cards-20250609091006.json",'r', encoding="utf-8") as f:
    json_reader = json.load(f)
    for card in json_reader:
        id = card["id"]
        lang = card["lang"]
        set = card["set"]
        col_number = card["scryfall_uri"].split("/")[5]
        
        # print(set + col_number)

        name = card["name"]
        set_name = card["set_name"]
        if not col_number.isdigit() and not (set == "plst"):
            print(card["scryfall_uri"])
            print(set, set_name, name)
            print(col_number)
            count += 1

        
        # break
print(count)




