from flask import Flask, render_template, request, send_file, url_for
from flask_sitemapper import Sitemapper
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
from io import BytesIO
import os
import requests
import textwrap

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
        "long_description": "Bali é a ilha dos deuses, com florestas tropicais, arrozais em terraços, templos ancestrais e uma cultura única. Perfeita para quem busca espiritualidade, aventura e relaxamento.",
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
        "long_description": "A Costa Rica é um paraíso de biodiversidade, com florestas tropicais, vulcões, praias do Pacífico e do Caribe. Ideal para ecoturismo e aventura.",
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
        "long_description": "Santorini é a jóia do Egeu, famosa pelas suas casas brancas com cúpulas azuis, pores do sol sobre a caldeira e vinhedos vulcânicos. É o destino romântico por excelência.",
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
        "long_description": "A Riviera Maya e Cancún oferecem o melhor do Caribe mexicano: praias de areia branca, águas turquesa, uma rica herança maia e cenotes impressionantes. É o destino perfeito para quem quer combinar descanso, aventura e cultura.",
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
# Função auxiliar para desenhar parágrafos com quebra automática
# -----------------------------
def draw_paragraph(c, text, x, y, max_width=450, font_name='Helvetica', font_size=10, leading=14):
    """
    Desenha um parágrafo com quebra automática de linhas.
    Retorna o novo y após o último texto desenhado.
    """
    if not text or text == '—':
        c.drawString(x, y, '—')
        return y - leading

    c.setFont(font_name, font_size)
    # Divide por quebras de linha manuais
    paragraphs = text.split('\n')
    current_y = y
    for para in paragraphs:
        if not para.strip():
            current_y -= leading
            continue
        # Estima número máximo de caracteres por linha (baseado na largura)
        max_chars = int(max_width / (font_size * 0.55))
        wrapped = textwrap.wrap(para, width=max_chars)
        for line in wrapped:
            c.drawString(x, current_y, line)
            current_y -= leading
    return current_y

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
    num_pessoas = request.form.get('num_pessoas', '1')
    valor_total = request.form.get('valor_total', '')
    voo = request.form.get('voo', '—')
    hotel = request.form.get('hotel', '—')
    regime = request.form.get('regime', 'All Inclusive')
    transfer = request.form.get('transfer', '—')
    seguro = request.form.get('seguro', '—')
    excursoes = request.form.get('excursões', '—')

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4  # 595.27 x 841.89 pts

    azul_escuro = HexColor("#0F2A4A")
    laranja = HexColor("#F97316")

    # Logo
    logo_path = os.path.join('static', 'logo.png')
    if os.path.exists(logo_path):
        c.drawImage(logo_path, 50, height - 80, width=60, height=60, mask='auto')
    else:
        try:
            logo_url = url_for('static', filename='logo.png', _external=True)
            response = requests.get(logo_url, timeout=5)
            if response.status_code == 200:
                logo = ImageReader(BytesIO(response.content))
                c.drawImage(logo, 50, height - 80, width=60, height=60, mask='auto')
        except:
            pass

    # Título
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(azul_escuro)
    c.drawString(130, height - 60, "Blue Palm Traveling")
    c.setFont("Helvetica", 12)
    c.setFillColor(HexColor("#4B5563"))
    c.drawString(130, height - 80, "Proposta de Viagem Personalizada")

    # Linha laranja
    c.setStrokeColor(laranja)
    c.setLineWidth(2)
    c.line(50, height - 95, width - 50, height - 95)

    y = height - 130
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(azul_escuro)
    c.drawString(50, y, "Dados do Cliente")
    y -= 20
    c.setFont("Helvetica", 10)
    c.setFillColor(HexColor("#1F2937"))
    c.drawString(50, y, f"Nome: {cliente}")
    y -= 18
    c.drawString(50, y, f"Email: {email}")
    y -= 18
    c.drawString(50, y, f"Data Ida: {data_ida}  |  Data Volta: {data_volta}")
    y -= 18
    c.drawString(50, y, f"Nº de pessoas: {num_pessoas}")

    # Valor total em destaque
    if valor_total:
        y -= 30
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(laranja)
        c.drawString(50, y, f"💰 Valor total da proposta: {valor_total} €")
        y -= 10
        c.setFont("Helvetica", 9)
        c.setFillColor(HexColor("#6B7280"))
        c.drawString(50, y, "Oferta válida por 7 dias. Sujeito a disponibilidade.")
    y -= 25

    # Voo
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(azul_escuro)
    c.drawString(50, y, "✈️ Voo")
    y -= 18
    y = draw_paragraph(c, voo, 50, y, max_width=500, font_size=10)

    # Alojamento
    y -= 15
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "🏨 Alojamento")
    y -= 18
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Hotel: {hotel}")
    y -= 16
    c.drawString(50, y, f"Regime: {regime}")
    y -= 8

    # Transfer
    y -= 25
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "🚗 Transfer")
    y -= 18
    y = draw_paragraph(c, transfer, 50, y, max_width=500)

    # Seguro
    y -= 15
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "🛡️ Seguro de Viagem")
    y -= 18
    y = draw_paragraph(c, seguro, 50, y, max_width=500)

    # Excursões
    y -= 15
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "🏝️ Excursões / Actividades")
    y -= 18
    y = draw_paragraph(c, excursoes, 50, y, max_width=500)

    # Rodapé (garantir mínimo de espaço)
    y = min(y, 70)  # se ultrapassar, mantém pelo menos 70
    y = max(y, 70)
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(HexColor("#6B7280"))
    c.drawString(50, y, "Blue Palm Traveling · Viagens sem complicações · @bluepalmtraveling")
    c.drawString(50, y - 15, "📞 +351 912 345 678  |  ✉️ ola@bluepalmtraveling.com")

    c.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f'proposta_{cliente.replace(" ", "_")}.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
