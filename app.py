from flask import Flask, render_template, request, send_file, url_for
from flask_sitemapper import Sitemapper
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import os
import requests

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
        "long_description": "As Maldivas são um arquipélago paradisíaco no oceano Índico...",
        "included": ["Voo directo de Lisboa", "Transfer privado (ida e volta)", "Hotel 5* tudo incluído", "Experiência de mergulho com snorkeling", "Sunset cruise com champanhe"],
        "common_tours": ["Snorkeling com tartarugas", "Passeio de barco com fundo de vidro", "Visita a ilha local", "Pesca noturna", "Safari ao pôr do sol com golfinhos"],
        "price": "1.790€",
        "old_price": "2.490€",
        "image": "https://images.pexels.com/photos/1450360/pexels-photo-1450360.jpeg",
        "badge": "Oferta relâmpago",
        "dates": "Mai – Nov 2026",
        "from": "Lisboa"
    },
    {
        "id": 2,
        "title": "Bali",
        "subtitle": "10 noites · Espiritualidade",
        "description": "Hotéis boutique, pequeno-almoço, tour cultural e spa.",
        "long_description": "Bali é a ilha dos deuses, com florestas tropicais...",
        "included": ["Voo com escala em Doha", "Transfer privado", "Hotel boutique 4* com pequeno-almoço", "Tour cultural com guia local", "Dia de spa tradicional"],
        "common_tours": ["Templo Tanah Lot ao pôr do sol", "Monkey Forest em Ubud", "Terraços de arroz Tegallalang", "Monte Batur sunrise trekking", "Mergulho em Amed"],
        "price": "1.390€",
        "old_price": "1.890€",
        "image": "https://images.pexels.com/photos/994605/pexels-photo-994605.jpeg",
        "badge": "-26%",
        "dates": "Mai – Nov 2026",
        "from": "Lisboa ou Porto"
    },
    {
        "id": 3,
        "title": "Costa Rica",
        "subtitle": "8 noites · Aventura",
        "description": "Eco‑lodges, transfers, zipline e floresta tropical.",
        "long_description": "A Costa Rica é um paraíso de biodiversidade...",
        "included": ["Voo com conexão", "Transfer privado", "Eco‑lodge 3* com pequeno-almoço", "Zipline em Monteverde", "Visita a parque nacional"],
        "common_tours": ["Caminhada na floresta nublada de Monteverde", "Arenal Volcano trek", "Canopy tour", "Observação de tartarugas marinhas", "Rafting no Rio Pacuare"],
        "price": "1.390€",
        "old_price": "1.890€",
        "image": "https://images.pexels.com/photos/12832297/pexels-photo-12832297.jpeg",
        "badge": "Últimas vagas",
        "dates": "Mai – Nov 2026",
        "from": "Lisboa"
    },
    {
        "id": 4,
        "title": "Santorini",
        "subtitle": "5 noites · Pôr do sol",
        "description": "Caverna tradicional em Oia, pequeno-almoço, jantar romântico e catamarã.",
        "long_description": "Santorini é a jóia do Egeu...",
        "included": ["Voo charter para Santorini", "Transfer privado", "Caverna tradicional em Oia com pequeno-almoço", "Jantar romântico com vista", "Catamarã com snorkeling"],
        "common_tours": ["Passeio de barco à volta da caldeira", "Visita a Akrotiri (Pompeia do Egeu)", "Prova de vinhos em vinícola local", "Caminhada de Fira para Oia", "Excursão a Nea Kameni (vulcão)"],
        "price": "790€",
        "old_price": "1.190€",
        "image": "https://images.pexels.com/photos/1285625/pexels-photo-1285625.jpeg",
        "badge": "-34%",
        "dates": "Mai – Out 2026",
        "from": "Lisboa, Porto ou Faro"
    },
    {
        "id": 5,
        "title": "Riviera Maya & Cancún",
        "subtitle": "7 noites · Praias do Caribe e cultura maia",
        "description": "Hotel tudo incluído, transfers, visita a Chichén Itzá e snorkeling em cenotes.",
        "long_description": "A Riviera Maya e Cancún oferecem o melhor do Caribe mexicano...",
        "included": ["Voo charter com bagagem", "Transfer privado ida e volta", "Hotel 5* tudo incluído", "Tour a Chichén Itzá com almoço", "Snorkeling em cenote sagrado"],
        "common_tours": ["Chichén Itzá e cenote Ik Kil", "Tulum e praia paradisíaca", "Coco Bongo (show noturno)", "Isla Mujeres com natação com golfinhos", "Snorkeling em Puerto Morelos"],
        "price": "1.390€",
        "old_price": "1.890€",
        "image": "https://images.pexels.com/photos/16116487/pexels-photo-16116487.jpeg",
        "badge": "-26%",
        "dates": "Mai – Nov 2026",
        "from": "Lisboa"
    }
]

# -----------------------------
# Rota principal (landing page)
# -----------------------------
@sitemapper.include()
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
# Rota do formulário de proposta
# -----------------------------
@app.route('/proposta')
def proposta_form():
    return render_template('proposta.html')

# -----------------------------
# Rota para gerar o PDF da proposta (usando ReportLab)
# -----------------------------
@app.route('/gerar_pdf', methods=['POST'])
def gerar_pdf():
    # Obter dados do formulário
    cliente = request.form.get('cliente', '')
    email = request.form.get('email', '')
    data_ida = request.form.get('data_ida', '')
    data_volta = request.form.get('data_volta', '')
    voo = request.form.get('voo', '—')
    hotel = request.form.get('hotel', '—')
    regime = request.form.get('regime', 'All Inclusive')
    transfer = request.form.get('transfer', '—')
    seguro = request.form.get('seguro', '—')
    excursoes = request.form.get('excursões', '—')

    # Criar buffer e canvas
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Tenta carregar o logo (se existir)
    logo_path = os.path.join('static', 'logo.png')
    if os.path.exists(logo_path):
        c.drawImage(logo_path, 50, height - 80, width=60, height=60, mask='auto')
    else:
        # Fallback: tenta carregar via URL
        try:
            logo_url = url_for('static', filename='logo.png', _external=True)
            response = requests.get(logo_url, timeout=5)
            if response.status_code == 200:
                logo = ImageReader(BytesIO(response.content))
                c.drawImage(logo, 50, height - 80, width=60, height=60, mask='auto')
        except:
            pass  # sem logo

    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(130, height - 60, "Blue Palm Traveling")
    c.setFont("Helvetica", 12)
    c.drawString(130, height - 80, "Proposta de Viagem Personalizada")

    # Linha de separação
    c.line(50, height - 95, width - 50, height - 95)

    # Dados do Cliente
    y = height - 130
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Dados do Cliente")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Nome: {cliente}")
    y -= 18
    c.drawString(50, y, f"Email: {email}")
    y -= 18
    c.drawString(50, y, f"Data Ida: {data_ida}")
    y -= 18
    c.drawString(50, y, f"Data Volta: {data_volta}")

    # Voo
    y -= 25
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Voo")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, voo[:90])

    # Alojamento
    y -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Alojamento")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Hotel: {hotel}")
    y -= 18
    c.drawString(50, y, f"Regime: {regime}")

    # Transfer
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Transfer")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, transfer[:80])

    # Seguro
    y -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Seguro de Viagem")
    y -= 20
    c.setFont("Helvetica", 10)
    text = seguro[:100]
    c.drawString(50, y, text)

    # Excursões
    y -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Excursões / Actividades Sugeridas")
    y -= 20
    c.setFont("Helvetica", 10)
    # Quebra de linha manual para texto longo
    lines = excursoes.split('\n')
    for line in lines:
        if len(line) > 85:
            # divide
            part1 = line[:85]
            part2 = line[85:]
            c.drawString(50, y, part1)
            y -= 15
            c.drawString(50, y, part2)
        else:
            c.drawString(50, y, line)
        y -= 15

    # Nota final
    y -= 30
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, y, "Esta proposta é válida por 7 dias. Para reservar ou mais informações, contacte-nos via WhatsApp.")
    y -= 20
    c.drawString(50, y, "Blue Palm Traveling · Viagens sem complicações · @bluepalmtraveling")

    c.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f'proposta_{cliente.replace(" ", "_")}.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
