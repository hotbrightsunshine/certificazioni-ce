import pyodbc 
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
    print(pyodbc.drivers())
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
        
        print(demo_query)
        execute(demo_query)
        
        
        
