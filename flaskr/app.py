from flask import Flask, render_template, request, session, redirect, url_for
from db import is_user, get_secret_key, register_ddt, query, is_logged, get_ddt_of_username, get_articles_with_ddt_number, insert_article
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
    print(request.form)
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

@app.route("/ddt/<int:ddtnum>")
def ddt(ddtnum:int):
    if is_logged(session) == False:
        return redirect("login")

    ddt = get_ddt_of_username(session['username'], ddtnum)

    return render_template("ddt_view.html", ddt=ddt)

@app.route("/ddt/<int:ddtnum>/articles", methods=['GET', 'POST'])
def articoli(ddtnum:int):
    if is_logged(session) == False:
        return redirect(url_for("login"))
    if request.method == 'POST':
        print(request.form)
        codice_interno = request.form['codice-interno']
        quantita = request.form['quantita']

        def it_or_false(req):
            if req in request.form:
                return True
            else:
                return False

        punzonatura = it_or_false('punzonatura')
        taglio = it_or_false('taglio')
        piegatura = it_or_false('piegatura')
        foratura = it_or_false('foratura')
        saldatura = it_or_false('saldatura')
        controlli_visivi = it_or_false('controlli-visivi')
        controlli_dimensionali = it_or_false('controlli-dimensionali')

        def bool_to_int(val:bool):
            if val:
                return 1
            else:
                return 0
        
        insert_article(
            ddt=ddtnum,
            filedic=" ",
            codice_interno=codice_interno,
            quantita=quantita,
            punzonatura=bool_to_int(punzonatura),
            taglio=bool_to_int(taglio),
            piegatura=bool_to_int(piegatura),
            foratura=bool_to_int(foratura),
            saldatura=bool_to_int(saldatura),
            controlli_visivi=bool_to_int(controlli_visivi),
            controlli_dimensionali=bool_to_int(controlli_dimensionali))
    
    articoli = get_articles_with_ddt_number(ddtnum)
    print(articoli)
#    if get_ddt_of_username(session['username'], ddtnum)
    #return articoli of ddtnum and username
    return render_template("articoli.html", articoli = articoli)
    
if __name__ == '__main__':
    app.run(host='192.168.219.129', port=5000, debug=True, threaded=False)
