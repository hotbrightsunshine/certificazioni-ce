from db import DB

class DDT:
    def get_of_username(username:str, num=None):
        if num == None:
            q = DB.select_star(f"testpython.cefddt0f", f"cedtidus='{username}' AND cedtata=' '")
            return q
        else:
            q = DB.select_star(f"testpython.CEFDDT0f", f"cedtidus='{username}' AND CEDTID={num} AND cedtata=' '")
            return q[0]

    def remove(num:int):
        DB.update_field("testpython.cefddt0f", "cedtata", "'r'", f"cedtid={num}")

    def get_ddt_from_record(ddt):
        dict_ddt = {
            'id' : int(ddt[0]),
            'datacertificazione' : ddt[1],
            'fornitore' : ddt[2],
            'numero' : ddt[3],
            'data' : ddt[4],
            'stato' : ddt[5]
        }
        return dict_ddt


    def get_ddts_from_records(ddts):
        ddtlist = []
        for ddt in ddts:
            ddtlist.append(DDT.get_ddt_from_record(ddt))
        return ddtlist

    def insert(date, fornitore, numddt, dataddt):
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
            DB.execute(q)
            return True
        except:
            return False
