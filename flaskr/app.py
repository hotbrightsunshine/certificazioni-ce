from flask import Flask, render_template, request, session, redirect, url_for
from db import is_user, get_secret_key, register_ddt, query, is_logged
from record_to_dict import get_ddts


## Flask App initialization
app = Flask(__name__)
app.secret_key = get_secret_key()

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
            return redirect(url_for("index"))
    print(fetched)
    return render_template('login.html', fetched=fetched,  username=session.get('username'))


## Logout
@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session['login'] = None
    session['username'] = None
    return redirect(url_for('index'))


## Index 
@app.route("/ddts")
def index():
    if is_logged(session) == False:
        return redirect(url_for("login"))
    username = session.get('username')
    login = session.get('login')
    ddtlist = query(f"SELECT * FROM testpython.cefddt0f WHERE cedtidus='{username}'")
    ddtlist_dict = get_ddts(ddtlist)
    return render_template('index.html', username = username, login = login, ddtlist=ddtlist_dict)

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
            return redirect(url_for('articoli'))
        else:
            error = "Controlla i dati e riprova"
    return render_template("ddt_compile.html", error=error, logged=is_logged(session))

@app.route("/ddt/<int:ddtnum>")
def ddt(ddtnum:int):
    if is_logged(session) == False:
        return redirect("login")
    #if ddt then show ddt
    #else return 404

@app.route("/ddt/<int:ddtum>/articles", methods=['GET', 'POST'])
def articoli(ddtnum:int):
    if is_logged(session) == False:
        return redirect(url_for("login"))

    #return articoli of ddtnum and username
    return render_template("articoli.html")
    
