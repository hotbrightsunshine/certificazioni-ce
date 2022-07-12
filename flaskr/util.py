class Util:
    # Traduce lo stato di un record in un valore booleano
    def status_to_int(val:str):
        if val == ' ':
            return True
        else:
            return False

    # Traduce i valori booleani in interi, seguendo la convenzione interna
    def bool_to_int(val:bool):
        if val:
            return 1
        else:
            return 0

    # Traduce i valori interi in booleani, seguendo la convenzione interna
    def int_to_bool(val:int):
        if val == 1:
            return True
        else:
            return False

    # Controlla se esiste un valore in un dizionario. Se esiste, ritorna True, altrimenti ritorna False.
    # (Utilizzato per il controllo delle checkbox)
    def it_or_false(req, key):
        try:
            req[key]
            return True
        except:
            return False
