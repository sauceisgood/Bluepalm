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
# Dados dos packs de viagem (com imagens externas e campos para modal)
# -----------------------------
packs = [
    {
        "id": 1,
        "title": "Maldivas",
        "subtitle": "7 noites · Luxo sobre águas",
        "description": "Resort overwater, pequeno-almoço, transferes e sunset cruise.",
        "long_description": "As Maldivas são um arquipélago paradisíaco no oceano Índico, conhecido pelas suas águas cristalinas, recifes de coral e luxuosos resorts overwater. É o destino ideal para quem procura privacidade, romance e contacto direto com a natureza marinha.",
        "included": ["Voo directo de Lisboa", "Transfer privado (ida e volta)", "Hotel 5* tudo incluído", "Experiência de mergulho com snorkeling", "Sunset cruise com champanhe"],
        "common_tours": ["Snorkeling com tartarugas", "Passeio de barco com fundo de vidro", "Visita a ilha local", "Pesca noturna", "Safari ao pôr do sol com golfinhos"],
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
        "long_description": "Bali é a ilha dos deuses, com florestas tropicais, arrozais em terraços, templos ancestrais e uma cultura única. Perfeita para quem busca espiritualidade, aventura e relaxamento.",
        "included": ["Voo com escala em Doha", "Transfer privado", "Hotel boutique 4* com pequeno-almoço", "Tour cultural com guia local", "Dia de spa tradicional"],
        "common_tours": ["Templo Tanah Lot ao pôr do sol", "Monkey Forest em Ubud", "Terraços de arroz Tegallalang", "Monte Batur sunrise trekking", "Mergulho em Amed"],
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
        "long_description": "A Costa Rica é um paraíso de biodiversidade, com florestas tropicais, vulcões, praias do Pacífico e do Caribe. Ideal para ecoturismo e aventura.",
        "included": ["Voo com conexão", "Transfer privado", "Eco‑lodge 3* com pequeno-almoço", "Zipline em Monteverde", "Visita a parque nacional"],
        "common_tours": ["Caminhada na floresta nublada de Monteverde", "Arenal Volcano trek", "Canopy tour", "Observação de tartarugas marinhas", "Rafting no Rio Pacuare"],
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
        "long_description": "Santorini é a jóia do Egeu, famosa pelas suas casas brancas com cúpulas azuis, pores do sol sobre a caldeira e vinhedos vulcânicos. É o destino romântico por excelência.",
        "included": ["Voo charter para Santorini", "Transfer privado", "Caverna tradicional em Oia com pequeno-almoço", "Jantar romântico com vista", "Catamarã com snorkeling"],
        "common_tours": ["Passeio de barco à volta da caldeira", "Visita a Akrotiri (Pompeia do Egeu)", "Prova de vinhos em vinícola local", "Caminhada de Fira para Oia", "Excursão a Nea Kameni (vulcão)"],
        "price": "1.190€",
        "old_price": "1.590€",
        "image": "https://images.pexels.com/photos/1285625/pexels-photo-1285625.jpeg",
        "badge": "-25%",
        "dates": "15 Set - 20 Set",
        "from": "Faro"
    },
    {
        "id": 5,
        "title": "Riviera Maya & Cancún",
        "subtitle": "7 noites · Praias do Caribe e cultura maia",
        "description": "Hotel tudo incluído, transfers, visita a Chichén Itzá e snorkeling em cenotes.",
        "long_description": "A Riviera Maya e Cancún oferecem o melhor do Caribe mexicano: praias de areia branca, águas turquesa, uma rica herança maia e cenotes impressionantes. É o destino perfeito para quem quer combinar descanso, aventura e cultura.",
        "included": ["Voo charter com bagagem", "Transfer privado ida e volta", "Hotel 5* tudo incluído", "Tour a Chichén Itzá com almoço", "Snorkeling em cenote sagrado"],
        "common_tours": ["Chichén Itzá e cenote Ik Kil", "Tulum e praia paradisíaca", "Coco Bongo (show noturno)", "Isla Mujeres com natação com golfinhos", "Snorkeling em Puerto Morelos"],
        "price": "1.490€",
        "old_price": "1.990€",
        "image": "https://images.pexels.com/photos/5409236/pexels-photo-5409236.jpeg",
        "badge": "-25%",
        "dates": "1 Out - 8 Out",
        "from": "Lisboa"
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
# (Opcional) Rota para blog no futuro - adicione aqui
# -----------------------------

if __name__ == '__main__':
    app.run(debug=True)
