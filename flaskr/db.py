import pyodbc
import os

class DB:
    # Apre una connessione con il database
    def get_connection():
        cnxn = pyodbc.connect('DRIVER={IBM i Access ODBC Driver};SYSTEM=lf;UID='+ os.getenv("DB_USERNAME") +';PWD='+os.getenv("DB_PASSWORD")+';')
        return cnxn

    # Invia una query (deprecato)
    def query(q:str):
        #print("QUERY: ", q)
        conn = DB.get_connection()
        cur = conn.cursor()
        cur.execute(q)
        fetched = cur.fetchall()
        cur.close()
        conn.close()
        return fetched

    # Invia una query e ritorna una mappa di valori { 'campo':valore }
    def query_dict(q:str):
        #print("QUERY: ", q)
        cursor = DB.get_connection().cursor().execute(q)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

    # Esegue una query INSERT o UPDATE 
    def execute(q:str):
        #print("EXECUTE: ", q)
        conn = DB.get_connection()
        conn.execute(q)
        conn.commit()
        conn.close()

    # Esegue una select selezionando solo uno o più campi
    def select_field(field, table, condition):
        q = f"SELECT {field} FROM {table} WHERE {condition}"
        return DB.query_dict(q)

    # Esegue una select selezionando tutti i campi
    def select_star(table, condition):
        return DB.select_field("*", table, condition)
    
    # Aggiorna un campo di una tabella
    def update_field(table, field, value, condition):
        q = f"UPDATE {table} SET {field} = {value} WHERE {condition}"
        DB.execute(q)


