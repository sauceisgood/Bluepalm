from flask import Flask, render_template
import os

app = Flask(__name__)

WHATSAPP_NUMBER = os.environ.get("WHATSAPP_NUMBER", "351936387563")

packs = [
    {
        "id": 1,
        "title": "Maldivas",
        "subtitle": "7 noites · Luxo sobre águas",
        "description": "Resort overwater, pequeno-almoço, transferes e sunset cruise.",
        "price": "1.890€",
        "old_price": "2.490€",
        "image": "https://images.pexels.com/photos/1450360/pexels-photo-1450360.jpeg?w=600&h=400&fit=crop",
        "badge": "Oferta relâmpago",
        "dates": "10 Mai - 17 Mai",
        "from": "Lisboa"
    },
    {
        "id": 2,
        "title": "Bali",
        "subtitle": "10 noites · Espiritualidade",
        "description": "Hotéis boutique, pequeno-almoço, tour cultural e spa.",
        "price": "1.490€",
        "old_price": "1.890€",
        "image": "https://images.pexels.com/photos/994605/pexels-photo-994605.jpeg",
        "badge": "-21%",
        "dates": "20 Jun - 30 Jun",
        "from": "Porto"
    },
    {
        "id": 3,
        "title": "Costa Rica",
        "subtitle": "8 noites · Aventura",
        "description": "Eco‑lodges, transfers, zipline e floresta tropical.",
        "price": "1.690€",
        "old_price": None,
        "image": "https://images.pexels.com/photos/3229659/pexels-photo-3229659.jpeg?w=600&h=400&fit=crop",
        "badge": "Últimas vagas",
        "dates": "5 Jul - 13 Jul",
        "from": "Lisboa"
    },
    {
        "id": 4,
        "title": "Santorini",
        "subtitle": "5 noites · Pôr do sol",
        "description": "Caverna tradicional em Oia, pequeno-almoço, jantar romântico e catamarã.",
        "price": "1.190€",
        "old_price": "1.590€",
        "image": "https://images.pexels.com/photos/1285625/pexels-photo-1285625.jpeg?w=600&h=400&fit=crop",
        "badge": "-25%",
        "dates": "15 Set - 20 Set",
        "from": "Faro"
    }
]

@app.route('/')
def index():
    for pack in packs:
        if pack.get("old_price") and pack["old_price"]:
            old_str = pack["old_price"].replace("€", "").replace(".", "").replace(",", ".").strip()
            new_str = pack["price"].replace("€", "").replace(".", "").replace(",", ".").strip()
            try:
                old_num = float(old_str)
                new_num = float(new_str)
                discount = int(round((old_num - new_num) / old_num * 100))
                pack["discount_percent"] = discount
            except:
                pack["discount_percent"] = None
        else:
            pack["discount_percent"] = None
    return render_template('index.html', packs=packs, whatsapp_number=WHATSAPP_NUMBER)

if __name__ == '__main__':
    app.run(debug=True)
