import dotenv
import os
import psycopg2

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
    return conn

def query(q:str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(q)
    fetched = cur.fetchall()
    cur.close()
    conn.close()
    return fetched

def is_user(name:str, passw:str):
    f = query(f"SELECT * FROM users WHERE utenteinterno='{name}' AND"
              f" password='{passw}'")
    return len(f) >= 1
