from flask import Flask, render_template
import os

app = Flask(__name__)

# Lê o número do WhatsApp de uma variável de ambiente (recomendado)
# ou usa um fallback para desenvolvimento
WHATSAPP_NUMBER = os.environ.get("WHATSAPP_NUMBER", "351936387563")

# Dados dos packs de viagem
packs = [
    {
        "id": 1,
        "title": "Escapada Maldivas",
        "subtitle": "7 noites · Luxo sobre águas cristalinas",
        "description": "Voo, resort overwater, pequeno-almoço incluso, transferes e sunset cruise.",
        "price": "1.890€",
        "old_price": "2.490€",
        "image": "https://images.unsplash.com/photo-1573848511323-95e51e8daacf?w=600&h=400&fit=crop",
        "badge": "Mais vendido"
    },
    {
        "id": 2,
        "title": "Paraíso Bali",
        "subtitle": "10 noites · Espiritualidade e natureza",
        "description": "Voos, hotéis boutique, pequeno-almoço, tour cultural e dia de spa.",
        "price": "1.490€",
        "old_price": "1.890€",
        "image": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=600&h=400&fit=crop",
        "badge": "Oferta especial"
    },
    {
        "id": 3,
        "title": "Costa Rica Selvagem",
        "subtitle": "8 noites · Aventura e biodiversidade",
        "description": "Voos, eco‑lodges, transfers, passeios em floresta tropical e boleia de zipline.",
        "price": "1.690€",
        "old_price": None,
        "image": "https://images.unsplash.com/photo-1585314062604-1a357de8b000?w=600&h=400&fit=crop",
        "badge": None
    },
    {
        "id": 4,
        "title": "Santorini Romance",
        "subtitle": "5 noites · Por do sol inesquecível",
        "description": "Voos, caverna tradicional em Oia, pequeno-almoço, jantar romântico e passeio de catamarã.",
        "price": "1.190€",
        "old_price": "1.590€",
        "image": "https://images.unsplash.com/photo-1570077188670-6cbad3df147f?w=600&h=400&fit=crop",
        "badge": "Romance"
    }
]

@app.route('/')
def index():
    return render_template('index.html', packs=packs, whatsapp_number=WHATSAPP_NUMBER)

# Não inclua app.run() aqui – a Vercel usa o objeto 'app' diretamente
