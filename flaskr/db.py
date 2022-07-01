import pyodbc
import os

class DB:
    def get_connection():
        cnxn = pyodbc.connect('DRIVER={IBM i Access ODBC Driver};SYSTEM=lf;UID='+ os.getenv("DB_USERNAME") +';PWD='+os.getenv("DB_PASSWORD")+';')
        return cnxn

    def query(q:str):
        #print("QUERY: ", q)
        conn = DB.get_connection()
        cur = conn.cursor()
        cur.execute(q)
        fetched = cur.fetchall()
        cur.close()
        conn.close()
        return fetched

    def query_dict(q:str):
        #print("QUERY: ", q)
        cursor = DB.get_connection().cursor().execute(q)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results


    def execute(q:str):
        print("EXECUTE: ", q)
        conn = DB.get_connection()
        conn.execute(q)
        conn.commit()
        conn.close()

    def select_field(field, table, condition):
        q = f"SELECT {field} FROM {table} WHERE {condition}"
        return DB.query_dict(q)

    def select_star(table, condition):
        return DB.select_field("*", table, condition)
    
    def update_field(table, field, value, condition):
        q = f"UPDATE {table} SET {field} = {value} WHERE {condition}"
        DB.execute(q)


