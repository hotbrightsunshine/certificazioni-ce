import dotenv
import os 
import psycopg2

def is_logged(session):
    if session['login']:
        return True
    else:
        return False

def get_secret_key():
    print(os.getenv("SECRET"))
    return os.getenv("SECRET")

def get_db_connection():
    dotenv.load_dotenv("../.env")
    conn = psycopg2.connect(
        host="192.168.110.161",
        database="itab",
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD")
    )
    conn.autocommit = True
    return conn

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
