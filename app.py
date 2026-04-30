from flask import Flask, render_template
from flask_sitemapper import Sitemapper
import os

app = Flask(__name__)

# Inicializar o Sitemapper
sitemapper = Sitemapper(app)
sitemapper.init_app(app)

# Número do WhatsApp (substitua pelo seu ou use variável de ambiente)
WHATSAPP_NUMBER = os.environ.get("WHATSAPP_NUMBER", "351936387563")

# -----------------------------
# Dados dos packs de viagem (com imagens locais)
# -----------------------------
packs = [
    {
        "id": 1,
        "title": "Maldivas",
        "subtitle": "7 noites · Luxo sobre águas",
        "description": "Resort overwater, pequeno-almoço, transferes e sunset cruise.",
        "price": "1.890€",
        "old_price": "2.490€",
        "image": "https://images.pexels.com/photos/1450360/pexels-photo-1450360.jpeg",
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
        "image": "https://images.pexels.com/photos/12832297/pexels-photo-12832297.jpeg",
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
        "image": "https://images.pexels.com/photos/1285625/pexels-photo-1285625.jpeg",
        "badge": "-25%",
        "dates": "15 Set - 20 Set",
        "from": "Faro"
    }
]

# -----------------------------
# Rota principal (landing page)
# -----------------------------
@sitemapper.include()
@app.route('/')
def index():
    # Calcular desconto percentual para cada pack
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

# -----------------------------
# Rota do Manual do Viajante
# -----------------------------
@sitemapper.include()
@app.route('/manual')
def manual():
    return render_template('manual.html')

# -----------------------------
# Rota do sitemap (para o Google)
# -----------------------------
@app.route('/sitemap.xml')
def sitemap():
    return sitemapper.generate()

# -----------------------------
# Se quiser criar uma rota /blog no futuro, basta adicionar:
# @sitemapper.include()
# @app.route('/blog')
# def blog():
#     return render_template('blog.html')
# -----------------------------

if __name__ == '__main__':
    app.run(debug=True)
