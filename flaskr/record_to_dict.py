def get_ddt(ddt):
    dict_ddt = {
        'id' : int(ddt[0]),
        'datacertificazione' : ddt[1],
        'fornitore' : ddt[2],
        'numero' : ddt[3],
        'data' : ddt[4],
        'stato' : ddt[5]
    }
    return dict_ddt


def get_ddts(ddts):
    ddtlist = []
    for ddt in ddts:
        print(ddt)
        ddtlist.append(get_ddt(ddt))
    return ddtlist
