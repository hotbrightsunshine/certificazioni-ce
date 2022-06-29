import pyodbc
import dotenv
import os

from record_to_dict import get_ddts, get_ddt

class DB:

    table_names = {
        'ddts': 'cefddt0f',
        'users': 'cefusr0f',
        'wps': 'cefwps0f',
        'articoli': 'cefart0f',
        'ordini': 'cefoda0f',
        'origini': 'cefori0f',
        'pf': 'cefpff0f',
        'prove_non_distruttive': 'cefpnd0f',
        'saldature': 'cefsal0f',
        'soggetti': 'cefsog0f',
        'wpqr': 'cefwqr0f',
        'equipaggiamenti': 'cefdev0f'
    }

    get_connection():
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

    def select_field(field, table, condition):
        q = f"SELECT {field} FROM {table} WHERE {condition}"
        return query(q)
    
    def select_star(table, condition):
        return select_field("*", table, condition)
    
    def update_field(table, field, value, condition):
        q = f"UPDATE {table} SET {field} = {value} WHERE {condition}"
        execute(q)


    def insert_article (ddt, codice_interno, quantita, filedic, punzonatura, piegatura, taglio, foratura, saldatura, controlli_visivi, controlli_dimensionali):
        q = f"INSERT INTO testpython.cefart0f (cearddtid, cearcdpa, cearqty, cearpunz, ceartagl, cearfora, cearpieg, cearsald, cearctdi, cearctvi, cearfile, cearata) VALUES ( '{ddt}', '{codice_interno}', {quantita}, {punzonatura}, {taglio}, {foratura}, {piegatura}, {saldatura}, {controlli_visivi}, {controlli_dimensionali}, ' ', ' ')"
        
        execute(q)

    def insert_ddt(date, fornitore, numddt, dataddt):
        q = f"""insert into testpython.cefddt0f (
        cedtcedt,
        cedtidus,
        cedtddtnr,
        cedtddtdt,
        cedtata)
        values (
        '{date}', '{fornitore}',
        '{numddt}', '{dataddt}', ' ' )"""
        try:
            execute(q)
            return True
        except:
            return False











    
