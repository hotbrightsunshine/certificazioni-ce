import pypyodbc
import dotenv
import os 


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
    
def get_secret_key():
    print(os.getenv("SECRET"))
    return os.getenv("SECRET")

def get_db_connection():
    connection = pypyodbc.conect(driver='{iSeries Access ODBC Driver}',
                                 system='192.168.110.5',uid='teststage',pwd="teststage")
    
    
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
    cur = conn.cursor()
    cur.execute(q)
    cur.close()
    conn.close()


def is_user(name:str, passw:str):
    f = query(f"SELECT * FROM users WHERE utenteinterno='{name}' AND"
              f" password='{passw}'")
    return len(f) >= 1

def register_ddt(date:str, fornitore:str, numddt:str, dataddt:str):
        demo_query = f"""insert into ddt (
        datacertificazione,
        supplier,
        ddtfornitorenumero,
        ddtfornitoredata )
        values (
        '{date}', '{fornitore}',
        {numddt}, '{dataddt}' );"""
        try:
            execute(demo_query)
            return True
        except:
            return False
