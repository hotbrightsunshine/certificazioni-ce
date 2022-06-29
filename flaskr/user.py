class User:
    def is_valid(name:str, passw:str):
        f = query(f"SELECT * FROM testpython.cefusr0f WHERE ceusid='{name}' AND"
                f" ceuspwd='{passw}'")
        return len(f) >= 1

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

    def get_equipaggiamenti_of_user(username:str):
        q = f"select * from testpython.cefdev0f where cedvcdfo='{username}'"
        return query(q)

    def get_soggetti_of_user(username:str):
        q = f"select * from testpython.cefsog0f where cefgcdfo='{username}'"
    
    def can_saldatura(username:str):
        try:
            return len(get_soggetti_of_user(username)) > 0 and len(get_equipaggiamenti_of_user(username)) > 0
        except:
            return False


