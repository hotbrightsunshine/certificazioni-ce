class Util:
    def status_to_int(val:str):
        if val == ' ':
            return True
        else:
            return False

    def bool_to_int(val:bool):
        if val:
            return 1
        else:
            return 0

    def int_to_bool(val:int):
        if val == 1:
            return True
        else:
            return False

    def it_or_false(req, key):
        try:
            req[key]
            return True
        except:
            return False
