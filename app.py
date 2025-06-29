from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import requests
import os

app = Flask(__name__)

# CORS Setup
CORS(app)

DATABASE_URL = os.environ.get("DATABASE_URL")
#DATABASE_URL = "postgresql://neondb_owner:npg_G4gqZLHj0wix@ep-green-tree-a1zfpwi0-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    print("Connected to Neon DB successfully!")
except Exception as e:
    print("Failed to connect to Neon DB")
    print(e)

@app.route('/')
def home():
    return "Welcome to the MTG Card API Backend (Flask + Neon + Scryfall)"


# Local price comparison from Neon
@app.route('/api/cards')
def get_cards():
    name_query = request.args.get('name', '')
    try:
        cursor.execute(
            """
            SELECT name, set, condition, foil, price, stock, store
            FROM cards
            WHERE name ILIKE %s
            """,
            (f"%{name_query}%",)
        )
        rows = cursor.fetchall()

        result = []
        for row in rows:
            result.append({
                "name": row[0],
                "set": row[1],
                "condition": row[2],
                "foil": row[3],
                "price": row[4],
                "stock": row[5],
                "store": row[6]
            })

        return jsonify(result)

    except Exception as e:
        print(e)
        return jsonify({"error": "Error fetching from database"}), 500
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({"error": "Username already exists"}), 409

        password_hash = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, password_hash)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "User registered successfully!"})

    except Exception as e:
        print(e)
        return jsonify({"error": "Database error"}), 500
    
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result and check_password_hash(result[0], password):
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"error": "Invalid username or password"}), 401

    except Exception as e:
        print(e)
        return jsonify({"error": "Database error"}), 500
    
#Fetch card info and image from Scryfall
@app.route('/api/scryfall')
def fetch_scryfall():
    name = request.args.get('name', '')
    url = f"https://api.scryfall.com/cards/named?fuzzy={name}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return jsonify({
            "name": data.get("name"),
            "set": data.get("set_name"),
            "image": data.get("image_uris", {}).get("normal", ""),
            "type": data.get("type_line"),
            "oracle_text": data.get("oracle_text")
        })
    else:
        return jsonify({"error": "Card not found in Scryfall"}), 404


# Run Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
