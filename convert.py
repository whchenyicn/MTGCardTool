import pandas as pd
import json

def load_and_label_csv(file_path, store_name):
    df = pd.read_csv(file_path, header=None, names=["name", "set", "condition", "foil", "price", "stock"])
    df["store"] = store_name
    return df

def main():
    # Load and label each CSV
    agora = load_and_label_csv("agorahobby_cardlist.csv", "AgoraHobby")
    gameshaven = load_and_label_csv("gameshaven_cardlist.csv", "GamesHaven")
    manapro = load_and_label_csv("manapro_cardlist.csv", "ManaPro")

    # Combine all
    df = pd.concat([agora, gameshaven, manapro], ignore_index=True)

    # Clean data
    df = df.dropna(subset=["name", "price"])  # Ensure name and price exist
    df["price"] = (df["price"].astype(float)).round().astype(int)  # Normalize price

    # Convert to records and export
    cards2 = df.to_dict(orient="records")
    with open("cards2.json", "w", encoding="utf-8") as f:
        json.dump(cards2, f, ensure_ascii=False, indent=2)

    print(f"✅ Converted {len(cards2)} cards to cards.json")

if __name__ == "__main__":
    main()