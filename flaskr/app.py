from flask import Flask, render_template, request, session, redirect, url_for
from db import is_user, get_secret_key, register_ddt, query, is_logget


## Flask App initialization
app = Flask(__name__)
app.secret_key = get_secret_key()


## Setting up sessions
app.config.from_object(__name__)

## Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    fetched=None
    alreadylogged = False
    if session.get("login"):
        return redirect(url_for("index"))
    elif request.method == "POST":
        if is_user(request.form['username'], request.form['password']):
            session['login'] = 'ok'
            session['username'] = request.form['username']
            return redirect(url_for("index"))
    print(fetched)
    return render_template('login.html', fetched=fetched, username=session.get('username'))


## Logout
@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session['login'] = None
    session['username'] = None
    return redirect(url_for('index'))


@app.route("/")
def index():
    username = session.get('username')
    login = session.get('login')
    ddtlist = query(f"SELECT * FROM ddt WHERE supplier='{username}'")
    return render_template('index.html', username = username, login = login, ddtlist=ddtlist)
@app.route("/ddt", methods=["POST", "GET"])
def ddt():
    error = None
    if not is_logged(session):
        redirect(url_for("login"))
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
    return render_template("ddt_compile.html", error=error)
