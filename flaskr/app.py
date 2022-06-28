from flask import Flask, render_template, request, session, redirect, url_for
from db import is_user, get_secret_key, register_ddt, query, is_logged, get_ddt_of_username, get_articles_with_ddt_number, insert_article, is_ce, get_article_and_insert_it, can_saldatura, remove_ddt
from record_to_dict import get_ddts


## Flask App initialization
app = Flask(__name__)
app.secret_key = get_secret_key()

## Flask Configuration
app.jinja_env.globals['login'] = is_logged(session)



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

@app.route("/ddt/<int:ddtnum>/delete", methods=['POST', 'GET'])
def removeddt(ddtnum:int):
    remove_ddt(ddtnum)
    return redirect(url_for('index'))

@app.route("/ddt/<int:ddtnum>")
def ddt(ddtnum:int):
    if is_logged(session) == False:
        return redirect("login")

    ddt = get_ddt_of_username(session['username'], ddtnum)

    return render_template("ddt_view.html", ddt=ddt)


@app.route("/ddt/<int:ddtnum>/articles", methods=['GET', 'POST'])
def articoli(ddtnum:int):
    articoli=[]
    if is_logged(session) == False:
        return redirect(url_for("login"))

    if request.method == 'POST':
        get_article_and_insert_it(request, ddtnum)
    
    print(request.form)
    articoli = get_articles_with_ddt_number(ddtnum)
    print("Articles with ddt number: ", articoli)
#    if get_ddt_of_username(session['username'], ddtnum)
    #return articoli of ddtnum and 
    return render_template("articoli.html", articles = articoli, ddtnum=ddtnum)


@app.route("/ddt/<int:ddtnum>/newarticle")
def newarticolo(ddtnum:int):
    if is_logged(session) == False:
        return redirect(url_for("login"))
    
    return render_template("new_article.html", ddtnum = ddtnum)


@app.route("/ddt/<int:ddtnum>/article/<int:artnum>")
def articolo(ddtnum:int, artnum:int):
    if is_logged(session) == False:
        return redirect(url_for("login"))
    lavorazioni = []
    return render_template("articolo_view.html", artnum = artnum, ddtnum = ddtnum, lavorazioni = lavorazioni)


@app.route("/ddt/<int:ddtnum>/article/<int:artnum>/newlavorazione")
def newlavorazione(ddtnum:int, artnum:int):
    if is_logged(session) == False:
        return redirect(url_for("login"))
    
    return render_template("new_lavorazione.html", artnum = artnum, ddtnum = ddtnum, can_saldatura = can_saldatura(session['username']))


if __name__ == '__main__':
    app.run(host='192.168.219.129', port=5000, debug=True, threaded=False)
