def get_ddt(ddt):
    dict_ddt = {
        'id' : ddt[0],
        'datacertificazione' : ddt[1],
        'numero' : ddt[2],
        'data' : ddt[3],
        'stato' : ddt[4],
        'fornitore' : ddt[5]
    }
    return dict_ddt

def get_ddts(ddt):
    ddtlist = []
    for i in ddt:
        ddtlist.append(get_ddt(i))
    return ddtlist
