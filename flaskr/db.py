import pyodbc 
import dotenv
import os 

from record_to_dict import get_ddts, get_ddt

def is_logged(session):
    try:
        return session['login'] == 'ok'
    except:
        return False

def is_ce(username):
    q = query(f'select * from testpython.cefusr0f where ceusid = \'{username}\'')
    q = q[0]
    ce = q[2]
    if ce == 'C':
        return True
    elif ce == 'F':
        return False
    else:
        return False
    
def get_username(session):
    if is_logged(session):
        return session['username']
    else:
        return None
    
def get_secret_key():
    
    return os.getenv("SECRET")

def get_db_connection():
    
    cnxn = pyodbc.connect('DRIVER={IBM i Access ODBC Driver};SYSTEM=lf;UID='+ os.getenv("DB_USERNAME") +';PWD='+os.getenv("DB_PASSWORD")+';')
    return cnxn
    
    
def query(q:str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(q)
    fetched = cur.fetchall()
    cur.close()
    conn.close()
    return fetched

def execute(q:str):
    conn = get_db_connection()
    conn.execute(q)
    conn.commit()
    conn.close()


def is_user(name:str, passw:str):
    f = query(f"SELECT * FROM testpython.cefusr0f WHERE ceusid='{name}' AND"
              f" ceuspwd='{passw}'")
    return len(f) >= 1

def register_ddt(date:str, fornitore:str, numddt:str, dataddt:str):
        demo_query = f"""insert into testpython.cefddt0f (
        cedtcedt,
        cedtidus,
        cedtddtnr,
        cedtddtdt,
        cedtata)
        values (
        '{date}', '{fornitore}',
        '{numddt}', '{dataddt}', ' ' )"""
        try: 
            
            execute(demo_query)
            return True
        except:
            return False


def get_ddt_of_username(username:str, num=None):
    if num == None:
        ddtlist = query(f"SELECT * FROM testpython.CEFDDT0F WHERE cedtidus='{username}'")

        return get_ddts(ddtlist)
    else:
        ddt = query(f"SELECT * FROM testpython.CEFDDT0F WHERE cedtidus='{username}' AND CEDTID={num} ")
        
        return get_ddt(ddt[0])

def get_articolo(art):
    return {
        'id': int(art[0]),
        'idcertificazione': int(art[1]),
        'codice_interno': art[2],
        'quantita': int(art[3]),
        'punzonatura': int_to_bool(art[4]),
        'foratura': int_to_bool(art[5]),
        'piegatura': int_to_bool(art[6]),
        'saldatura': int_to_bool(art[7]),
        'ctrldimensionali': int_to_bool(art[8]),
        'ctrlvisivi': int_to_bool(art[9]),
        'file': int_to_bool(art[10]),
        'stato': int_to_bool(art[11]),
    } 

def get_articoli(artlist):
    diclist = []
    for art in artlist:
        diclist.append(get_articolo(art))
    return diclist


def get_articles_with_ddt_number(num:int):
    articoli = query(f"SELECT * FROM testpython.cefart0f WHERE cearddtid = '{num}'")
    return get_articoli(articoli)

def status_to_int(val:str):
    if val == ' ':
        return True
    else:
        return False

def bool_to_int(val:bool):
    if val:
        return 1
    else:
        return 0

def int_to_bool(val:int):
    if val == 1:
        return True
    else:
        return False
    
def get_article_and_insert_it(request, ddtnum):
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
       

def insert_article (ddt, codice_interno, quantita, filedic, punzonatura, piegatura, taglio, foratura, saldatura, controlli_visivi, controlli_dimensionali):
    
    q = f"INSERT INTO testpython.cefart0f (cearddtid, cearcdpa, cearqty, cearpunz, ceartagl, cearfora, cearpieg, cearsald, cearctdi, cearctvi, cearfile, cearata) VALUES ( '{ddt}', '{codice_interno}', {quantita}, {punzonatura}, {taglio}, {foratura}, {piegatura}, {saldatura}, {controlli_visivi}, {controlli_dimensionali}, ' ', ' ')"
    
    execute(q)
