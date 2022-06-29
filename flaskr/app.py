from flask import Flask, render_template, request, session, redirect, url_for
from db import *
from record_to_dict import *


## Flask App iniprint(tialization
app = Flask(__name__)
app.secret_key = get_secret_key()


## Flask Configuration
app.jinja_env.globals['login'] = is_logged(session)


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

## Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    fetched=None
    if is_logged(session):
        return redirect(url_for("index"))
    elif request.method == "POST":
        if is_user(request.form['username'], request.form['password']):
            session['login'] = 'ok'
            session['username'] = request.form['username']
            session['certificazione'] = is_ce(session['username'])
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
    ddtlist = get_ddt_of_username(username, None)
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
        if register_ddt(
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
    remove_ddt(ddtnum)
    return redirect(url_for('index'))

## DDT Detailed View
@app.route("/ddt/<int:ddtnum>")
def ddt(ddtnum:int):
    if is_logged(session) == False:
        return redirect("login")

    ddt = get_ddt_of_username(session['username'], ddtnum)

    return render_template("ddt_view.html", ddt=ddt)


## Articoli
@app.route("/ddt/<int:ddtnum>/articles", methods=['GET', 'POST'])
def articoli(ddtnum:int):
    articoli=[]
    if is_logged(session) == False:
        return redirect(url_for("login"))

    if request.method == 'POST':
        get_article_and_insert_it(request, ddtnumatura)
    print(request.form)
    articoli = get_articles_with_ddt_number(ddtnum)
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
    return render_template("articolo_view.html", artnum = artnum,
                           ddtnum = ddtnum, lavorazioni = lavorazioni)


## Articolo > SaveLavorazioni
@app.route("/ddt/<int:ddtnum>/article/<int:artnum>/lavorazioni", methods=["GET", "POST"])
def update_lavorazioni_articolo(ddtnum:int, artnum:int):
    if is_logged(session) == False:
        return redirect(url_for("login"))
    taglio = it_or_false(request.form, "Taglio")
    punzonatura = it_or_false(request.form, "Punzonatura")
    saldatura = it_or_false(request.form, "Saldatura")
    piegatura = it_or_false(request.form, "Piegatura")
    foratura= it_or_false(request.form, "Foratura")

    update_lavorazioni(artnum, taglio, punzonatura, saldatura, piegatura, foratura)

    return redirect(url_for("articolo", ddtnum=ddtnum, artnum=artnum))


## Main
if __name__ == '__main__':
    app.run(host='192.168.219.129', port=5000, debug=True, threaded=False)
