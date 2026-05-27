from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'tajny_klic_veselsky_geografie'

@app.route('/', methods=['GET', 'POST'])
def index():
    chyba = None
    if request.method == 'POST':
        jmeno = request.form.get('jmeno')
        trida = request.form.get('trida')
        datum = request.form.get('datum')
        typ_omluvy = request.form.get('typ_omluvy')
        duvod = request.form.get('duvod')

        if not jmeno or not trida or not datum or not typ_omluvy or not duvod:
            chyba = "Pro vygenerování platné zeměpisné omluvy musíš vyplnit všechna pole!"
        else:
            # 1. Dynamický úvod podle toho, o co žák žádá
            uvody = {
                "absence": "tímto oficiálně žádám o omluvení mé neúčasti v hodině zeměpisu.",
                "ukol": "tímto se Vám hluboce omlouvám, ale bohužel nemám vypracovaný zadaný domácí úkol.",
                "zkouseni": "tímto Vás s maximálním respektem žádám, abyste mě dnes nevyvolával k ústnímu zkoušení."
            }
            zvoleny_uvod = uvody.get(typ_omluvy, "tímto Vás žádám o shovívavost.")

            # 2. Slovník všech absurdních výmluv (nyní fungují pro cokoliv)
            formalni_texty = {
                "sutry": "Byl jsem totiž nucen provést neodkladný geologický průzkum terénu za účelem sběru unikátních litosférických vzorků (lidově 'šutrů').",
                "krtek": "Dostal jsem se do nevyprovokované fyzické konfrontace s mimořádně agresivním zástupcem druhu Talpa europaea (krtek obecný), který mi zkřížil cestu.",
                "koaly": "Má lokace byla zasažena náhlou a zcela nečekanou plošnou invazí australských vačnatců druhu Phascolarctos cinereus (koala).",
                "alkohol": "Došlo u mě k těžké indispozici vlivem neúmyslné a čistě výzkumné degustace nadměrného množství roztoku ethanolu.",
                "lidl": "Byl jsem na neúnosně dlouhou dobu uvězněn v časoprostorové anomálii, která se vytvořila u pokladny v nadnárodním řetězci Lidl během mého strategického nákupu ranního pečiva.",
                "banan": "Došlo k fatálnímu selhání koeficientu tření mezi mou obuví a zbytkem tropického plodu (Musa sapientum).",
                "krokodyl": "Byl jsem nucen aplikovat krizové defenzivní strategie vůči agresivnímu zástupci řádu Crocodilia.",
                "voda": "Došlo k závažnému kognitivnímu přetížení při zjištění empirického faktu, že voda je skutečně mokrá.",
                "maslo": "Došlo ke kritickému zalehnutí mých dýchacích cest viskózní arašídovou hmotou."
            }
            
            zvoleny_text = formalni_texty.get(duvod, "Záhadné časoprostorové anomálie mi překazily plány.")
            
            # 3. Uložení výsledku do session
            session['omluvenka'] = {
                'jmeno': jmeno,
                'trida': trida,
                'datum': datum,
                'uvod': zvoleny_uvod,
                'text': zvoleny_text,
            }
            return redirect(url_for('vysledek'))
            
    return render_template('index.html', chyba=chyba)

@app.route('/omluvenka')
def vysledek():
    data = session.get('omluvenka')
    if not data:
        return redirect(url_for('index'))
    return render_template('omluvenka.html', data=data)

@app.route('/o-aplikaci')
def o_aplikaci():
    return render_template('info.html')

if __name__ == '__main__':
    app.run(debug=True)