class DDT:
    def get_of_username(username:str, num=None):
        if num == None:
            ddtlist = query(f"SELECT * FROM testpython.CEFDDT0F WHERE cedtidus='{username}' AND cedtata=' '")
            return get_ddts(ddtlist)
        else:
            ddt = query(f"SELECT * FROM testpython.CEFDDT0F WHERE cedtidus='{username}' AND CEDTID={num} AND cedtata=' ' ")
            return get_ddt(ddt[0])

    def remove(num:int):
        q = f"update testpython.cefddt0f set cedtata='r' where cedtid={num}"
        execute(q)
