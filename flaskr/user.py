from db import DB

class User:
    def is_valid(name:str, passw:str):
        f = DB.select_star("testpython.cefusr0f", f"ceusid='{name}' AND ceuspwd='{passw}'")
        return len(f) >= 1

    def is_ce(username):
        q = DB.select_star("testpyhon.cefusr0f", f"ceusid = '{username}'")
        q = q[0]
        ce = q[2]
        if ce == 'C':
            return True
        elif ce == 'F':
            return False
        else:
            return False

    def get_equipaggiamenti_of_user(username:str):
        return DB.select_star("testpython.cefdev0f", f"cedvcdfo='{username}'")

    def get_soggetti_of_user(username:str):
        return DB.select_star("testpython.cefsog0f", f"where cefgcdfo='{username}'")
    
    def can_saldatura(username:str):
        try:
            return len(User.get_soggetti_of_user(username)) > 0 and len(User.get_equipaggiamenti_of_user(username)) > 0
        except:
            return False


