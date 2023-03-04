import requests
import json
def config():
    url = "http://localhost:8000/cards.json"
    data = requests.get(url)
    data = data.json()
    for card in data:
        for card_name in card:
            if "Raigeki" == card_name:
                card_details = card[card_name]
                details = card_details["Details"]
                for detail in details:
                    for set_code in detail:
                        rarity = detail[set_code]["rarity"]
                        with open("config.json", "r") as f:
                            data = json.load(f)
                        for key in data:
                            if rarity == key:
                                rarity = data[key]
                        print(rarity)

config()