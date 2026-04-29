from flask import Flask, render_template
import os

app = Flask(__name__)

WHATSAPP_NUMBER = os.environ.get("WHATSAPP_NUMBER", "351936387563")

packs = [ ... ]  # (já tens os packs, mantém)

@app.route('/')
def index():
    # (calcula descontos etc.) – mantém o teu código existente
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

@app.route('/manual')
def manual():
    return render_template('manual.html')

if __name__ == '__main__':
    app.run(debug=True)
