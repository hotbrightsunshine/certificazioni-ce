import os

from flask import Flask, render_template, request, session, redirect, url_for

from db import DB
from ddt import DDT
from articolo import Articolo
from util import Util
from user import User

def is_logged(session):
    try:
        return session['login'] == 'ok'
    except:
        return False


def get_username(session):
    if is_logged(session):
        return session['username']
    else:
        return None


## Flask App iniprint(tialization
app = Flask(__name__)
app.secret_key = os.get_env("SECRET")


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
    print(fetched)
    print(request.form)
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
    print(username)
    ddtlist = DDT.get_of_username(username, None)
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
    print(request.form)
    articoli = Articolo.get_with_ddt_number(ddtnum)
    return render_template("articoli.html", articles = articoli, ddtnum=ddtnum)


## Nuovo Articolo
@app.route("/ddt/<int:ddtnum>/newarticle")
def newarticolo(ddtnum:int):
    if is_logged(session) == False:
        return redirect(url_for("login"))
    return render_template("new_article.html", ddtnum = ddtnum)


## Articolo Detailed View
@app.route("/ddt/<int:ddtnum>/article/<int:artnum>")
def articolo(ddtnum:int, artnum:int):
    if is_logged(session) == False:
        return redirect(url_for("login"))
    lavorazioni = []
    return render_template("articolo_view.html", artnum = artnum, ddtnum = ddtnum, lavorazioni = lavorazioni)


## Articolo > SaveLavorazioni
@app.route("/ddt/<int:ddtnum>/article/<int:artnum>/lavorazioni", methods=["GET", "POST"])
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


## Main
if __name__ == '__main__':
    app.run(host='192.168.219.129', port=5000, debug=True, threaded=False)
