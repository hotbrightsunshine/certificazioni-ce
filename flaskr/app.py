import os
from ossaudiodev import control_labels

from flask import Flask, render_template, request, session, redirect, url_for

from db import DB
from ddt import DDT
from articolo import Articolo
from util import Util
from user import User

# Controlla che l'utente sia loggato
def is_logged(session):
    try:
        return session['login'] == 'ok'
    except:
        return False

# Ritorna l'username dell'utente
def get_username(session):
    if is_logged(session):
        return session['username']
    else:
        return None


## Flask App: Inizializzazione
app = Flask(__name__)
app.secret_key = os.getenv("SECRET")


## Flask Configuration
app.jinja_env.globals['login'] = is_logged(session)


## Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    fetched=None
    if is_logged(session):
        return redirect(url_for("index"))
    elif request.method == "POST":
        if User.is_valid(request.form['username'], request.form['password']):
            session['login'] = 'ok'
            session['username'] = request.form['username']
            session['certificazione'] = User.is_ce(session['username'])
            return redirect(url_for("index"))
    return render_template('login.html', fetched=fetched,  username=session.get('username'))


## Logout
@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session['login'] = None
    session['username'] = None
    return redirect(url_for('index'))


## Index 
@app.route("/")
def index():
    if is_logged(session) == False:
        return redirect(url_for("login"))
    username = session.get('username')
    login = session.get('login')
    ddtlist = DDT.get_of_username(session.get('username'))
    return render_template('index.html', username = username, login = login, ddtlist=ddtlist)


## DTT Form 
@app.route("/newddt", methods=["POST", "GET"])
def newddt():
    error = None
    if is_logged(session) == False:
        return redirect(url_for("login"))
    if request.method =="POST":
        datacert = request.form["datacert"]
        username = session.get("username")
        numero = request.form["numero"]
        date = request.form["date"]
        if DDT.insert(
                datacert,
                username,
                numero,
                date):
            return redirect(url_for('index'))
        else:
            error = "Controlla i dati e riprova"
    return render_template("ddt_compile.html", error=error, logged=is_logged(session))

## Remove DDT Redirect
@app.route("/ddt/<int:ddtnum>/delete", methods=['POST', 'GET'])
def removeddt(ddtnum:int):
    DDT.remove(ddtnum)
    return redirect(url_for('index'))

## DDT Detailed View
@app.route("/ddt/<int:ddtnum>")
def ddt(ddtnum:int):
    if is_logged(session) == False:
        return redirect("login")

    ddt = DDT.get_of_username(session['username'], ddtnum)

    return render_template("ddt_view.html", ddt=ddt)


## Articoli
@app.route("/ddt/<int:ddtnum>/articles", methods=['GET', 'POST'])
def articoli(ddtnum:int):
    articoli=[]
    if is_logged(session) == False:
        return redirect(url_for("login"))

    if request.method == 'POST':
        Articolo.get_and_insert(request, ddtnum)

    articoli = Articolo.get_with_ddt_number(ddtnum)
    return render_template("articoli.html", articles = articoli, ddtnum=ddtnum)


## Nuovo Articolo
@app.route("/ddt/<int:ddtnum>/newarticle")
def newarticolo(ddtnum:int):
    if is_logged(session) == False:
        return redirect(url_for("login"))
    return render_template("new_article.html", ddtnum = ddtnum)


## Delete Articolo
@app.route("/ddt/<int:ddtnum>/article/<int:artnum>/delete")
def delete_articolo(ddtnum:int, artnum:int):
    if is_logged(session) == False:
        return redirect(url_for("login"))
    Articolo.delete(artnum)
    return redirect(url_for("articoli", ddtnum=ddtnum))


## Articolo Detailed View
@app.route("/ddt/<int:ddtnum>/article/<int:artnum>")
def articolo(ddtnum:int, artnum:int):
    if is_logged(session) == False:
        return redirect(url_for("login"))

    materiali = DB.select_star("testpython.cefori0f", f"ceoridar='{artnum}' AND ceorata = ' '")
    isce = User.is_ce(session.get('username'))
    can_saldatura = User.can_saldatura(session.get('username'))

    articolo=Articolo.get(artnum)
    articolo_quantita = articolo['CEARQTY']

    # Lista degli ordini
    ordini=Articolo.get_orders_of(artnum)

    # Quantità complessiva degli ordini
    orders_sum = Articolo.get_sum_of_orders(ordini)

    err_apporto_mancante = Articolo.is_apporto_mancante(artnum)

    err_troppi_ordini = orders_sum > articolo_quantita
    max_ordini = articolo_quantita - orders_sum

    is_difference_zero=articolo_quantita == orders_sum
    
    try:
        saldatura = DB.select_star("testpython.cefsal0f", f"cesaarid={artnum}")[0]
    except:
        saldatura = []

    equip = DB.select_star("testpython.cefdev0f", f"cedvcdfo='{get_username(session)}'")
    sald = DB.select_star("testpython.cefsog0f", f"cesgcdfo='{get_username(session)}'")
    wps = DB.select_star("testpython.cefwps0f", f"cewscdfo='{get_username(session)}'")
    wpqr = DB.select_star("testpython.cefwqr0f", f"cewrcdfo='{get_username(session)}'")

    return render_template("articolo_view.html", artnum = artnum, ddtnum = ddtnum, 
        materiali=materiali, isce=isce, can_saldatura=can_saldatura, 
        err_apporto_mancante=err_apporto_mancante, 
        equipaggiamento = equip,
        saldatori = sald,
        wpss = wps,
        wpqrs = wpqr,
        saldatura = saldatura,
        ordini=ordini, err_troppi_articoli=err_troppi_ordini, 
        max_qty=max_ordini, is_difference_zero=is_difference_zero, articolo=articolo)


## Articolo > SaveLavorazioni
@app.route("/ddt/<int:ddtnum>/article/<int:artnum>/lavorazioni", methods=["POST"])
def update_lavorazioni_articolo(ddtnum:int, artnum:int):
    if is_logged(session) == False:
        return redirect(url_for("login"))
    taglio = Util.it_or_false(request.form, "Taglio")
    punzonatura = Util.it_or_false(request.form, "Punzonatura")
    saldatura = Util.it_or_false(request.form, "Saldatura")
    piegatura = Util.it_or_false(request.form, "Piegatura")
    foratura= Util.it_or_false(request.form, "Foratura")

    Articolo.update_lavorazioni(artnum, taglio, punzonatura, saldatura, piegatura, foratura)

    return redirect(url_for("articolo", ddtnum=ddtnum, artnum=artnum))


## Articolo > SaveControlli
@app.route("/ddt/<int:ddtnum>/article/<int:artnum>/controlli", methods=["POST"])
def update_controlli(ddtnum:int, artnum:int):
    if is_logged(session) == False:
        return redirect(url_for("login"))
    controlli_dimensionali = Util.it_or_false(request.form, "controlli-dimensionali")
    controlli_visivi = Util.it_or_false(request.form, "controlli-visivi")

    Articolo.update_controlli(artnum, controlli_dimensionali, controlli_visivi)
    return redirect(url_for("articolo", ddtnum=ddtnum, artnum=artnum))


## Articolo > SaveMaterialeCollaudo
@app.route("/ddt/<int:ddtnum>/article/<int:artnum>/materialecollaudo", methods=["POST"])
def add_materiale_collaudo(ddtnum:int, artnum:int):
    if is_logged(session) == False:
        return redirect(url_for("login"))

    colata=request.form['numeroColata']
    certcollaudo=request.form['certificatoCollaudo']
    datacollaudo=request.form['dataCertificato']

    tipomateriale = request.form['tipoMateriale2']

    dop=Util.it_or_false(request.form, "dop")
    dop=Util.bool_to_int(dop)
    
    Articolo.update_materiale_collaudo(artnum, colata, certcollaudo, datacollaudo, tipomateriale, dop)

    return redirect(url_for("articolo", ddtnum=ddtnum, artnum=artnum))


## Articolo > SaveMaterialeContoLavorazione
@app.route("/ddt/<int:ddtnum>/article/<int:artnum>/materialecontolavorazione", methods=["POST"])
def add_materiale_conto_lavorazione(ddtnum:int, artnum:int):
    if is_logged(session) == False:
        return redirect(url_for("login"))

    codicecomponente=request.form['codiceComponente']
    numerocolata=request.form['numeroColata']
    punzonatura=request.form['punzonatura']
    tipomateriale = request.form['tipoMateriale']
        

    Articolo.update_materiale_conto_lavorazione(artnum, codicecomponente, numerocolata, punzonatura, tipomateriale)

    return redirect(url_for("articolo", ddtnum=ddtnum, artnum=artnum))


## Articolo > Add Order
@app.route("/ddt/<int:ddtnum>/article/<int:artnum>/ordine", methods=["POST"])
def add_order(ddtnum, artnum):
    if is_logged(session) == False:
        return redirect(url_for("login"))
    
    numero = request.form['numeroOrdine']
    quantita = request.form['quantitaOrdine']
    data = request.form['dataOrdine']

    Articolo.insert_order(artnum, numero, data, quantita)

    return redirect(url_for("articolo", ddtnum=ddtnum, artnum=artnum))  


# Quantità
@app.route("/ddt/<int:ddtnum>/article/<int:artnum>/quantita", methods=["POST"])
def set_quantity(ddtnum, artnum):
    if is_logged(session) == False:
        return redirect(url_for("login"))
    
    DB.update_field("testpython.cefart0f", "cearqty", f"{request.form['qty']}", f"cearid={artnum}")

    return redirect(url_for("articolo", ddtnum=ddtnum, artnum=artnum))  


#Saldatura
@app.route("/ddt/<int:ddtnum>/article/<int:artnum>/saldatura", methods=["POST"])
def set_saldatura(ddtnum, artnum):
    if is_logged(session) == False:
        return redirect(url_for("login"))

    saldatore1 = request.form['sald1']
    saldatore2 = request.form['sald2']

    equip = request.form['equip']
    wps = request.form['wps']
    wpqr1 = request.form['wpqr1']
    wpqr2 = request.form['wpqr2']
    if wpqr2 == wpqr1:
        wpqr2 = 0

    sald = DB.select_star("testpython.cefsal0f", f"cesaarid='{artnum}'")
    if sald == []:
        DB.execute(f"""INSERT INTO testpython.cefsal0f (
            cesaarid, cesas1id, cesas2id, cesar1id, cesar2id, cesawsid,
            cesadeid, cesaata) VALUES (
                {artnum}, {saldatore1}, {saldatore2}, 
                {wpqr1}, {wpqr2}, {wps}, {equip}, ' ')""")
    else:
        DB.update_field("testpython.cefsal0f", "cesas1id", f"{saldatore1}", f"cesaarid={artnum}")
        DB.update_field("testpython.cefsal0f", "cesas2id", f"{saldatore2}", f"cesaarid={artnum}")
        DB.update_field("testpython.cefsal0f", "cesar1id", f"{wpqr1}", f"cesaarid={artnum}")
        DB.update_field("testpython.cefsal0f", "cesar2id", f"{wpqr2}", f"cesaarid={artnum}")
        DB.update_field("testpython.cefsal0f", "cesawsid", f"{wps}", f"cesaarid={artnum}")
        DB.update_field("testpython.cefsal0f", "cesadeid", f"{equip}", f"cesaarid={artnum}")
    return redirect(url_for("articolo", ddtnum=ddtnum, artnum=artnum))  


## Delete Ordine
@app.route("/ddt/<int:ddtnum>/article/<int:artnum>/deleteordine/<int:ordnum>", methods=['POST', "GET"])
def delete_ordine(ddtnum:int, artnum:int, ordnum:int):
    if is_logged(session) == False:
        return redirect(url_for("login"))
    Articolo.delete_ordine(ordnum)
    return redirect(url_for("articolo", artnum=artnum, ddtnum=ddtnum))


## Delete Materiale
@app.route("/ddt/<int:ddtnum>/article/<int:artnum>/deletemateriale/<int:matnum>", methods=['POST', "GET"])
def delete_materiale(ddtnum:int, artnum:int, matnum:int):
    if is_logged(session) == False:
        return redirect(url_for("login"))
    Articolo.delete_materiale(matnum)
    return redirect(url_for("articolo", artnum=artnum, ddtnum=ddtnum))

## Main
if __name__ == '__main__':
    app.run(host='192.168.219.129', port=5000, debug=True, threaded=False)
