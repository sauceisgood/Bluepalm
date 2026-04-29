from flask import Flask, render_template
import os

app = Flask(__name__)

# Número do WhatsApp (substitua pelo seu ou use variável de ambiente)
WHATSAPP_NUMBER = os.environ.get("WHATSAPP_NUMBER", "351936387563")

packs = [
    {
        "id": 1,
        "title": "Maldivas",
        "subtitle": "7 noites · Luxo sobre águas",
        "description": "Resort overwater, pequeno-almoço, transferes e sunset cruise.",
        "price": "1.890€",
        "old_price": "2.490€",
        "image": "https://images.unsplash.com/photo-1573848511323-95e51e8daacf?w=600&h=400&fit=crop",
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
        "image": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=600&h=400&fit=crop",
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
        "image": "https://images.unsplash.com/photo-1585314062604-1a357de8b000?w=600&h=400&fit=crop",
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
        "image": "https://images.unsplash.com/photo-1570077188670-6cbad3df147f?w=600&h=400&fit=crop",
        "badge": "-25%",
        "dates": "15 Set - 20 Set",
        "from": "Faro"
    }
]

@app.route('/')
def index():
    # Calcular desconto percentual para cada pack
    for pack in packs:
        if pack.get("old_price") and pack["old_price"]:
            # Limpar string do preço (ex: "1.890€" -> 1890)
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

# Não incluir app.run() quando for para a Vercel
if __name__ == '__main__':
    app.run(debug=True)
