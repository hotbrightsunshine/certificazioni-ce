from db import DB

class User:
    # Controlla che le credenziali di accesso siano valide 
    def is_valid(name:str, passw:str):
        f = DB.select_star("testpython.cefusr0f", f"ceusid='{name}' AND ceuspwd='{passw}' AND ceusata=' '")
        return len(f) >= 1

    # Controlla se il fornitore è CE
    def is_ce(username):
        q = DB.select_star("testpython.cefusr0f", f"ceusid = '{username}'")
        q = q[0]
        ce = q['CEUSTIFO']
        if ce == 'C':
            return True
        elif ce == 'F':
            return False
        else:
            return False

    # Ritorna una lista di equipaggiamenti dato l'utente
    def get_equipaggiamenti_of_user(username:str):
        return DB.select_star("testpython.cefdev0f", f"cedvcdfo='{username}'")

    # Ritorna una lista di saldatori dato l'utente
    def get_soggetti_of_user(username:str):
        return DB.select_star("testpython.cefsog0f", f"cesgcdfo='{username}'")
    
    # Se l'utente ha la facoltà di saldare ritorna True, altrimenti False 
    def can_saldatura(username:str):
        try:
            return (len(User.get_soggetti_of_user(username)) > 0) and (len(User.get_equipaggiamenti_of_user(username)) > 0)
        except:
            return False

    def get_tipo(username:str):
        u = DB.select_star("testpython.cefusr0f", f"ceusid='{username}'")
        if u[0]['CEUSTIPO'] == 'F':
            return 'fornitore'
        elif u[0]['CEUSTIPO'] == 'S':
            return 'interno'
        else:
            return 'ricevimento'


