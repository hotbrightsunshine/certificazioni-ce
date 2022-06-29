from db import *

class Articolo:
    def get_from_record(record):
        return {
            'id': int(record[0]),
            'idcertificazione': int(record[1]),
            'codice_interno': art[2],
            'quantita': int(art[3]),
            'punzonatura': int_to_bool(art[4]),
            'foratura': int_to_bool(art[5]),
            'piegatura': int_to_bool(art[6]),
            'saldatura': int_to_bool(art[7]),
            'ctrldimensionali': int_to_bool(art[8]),
            'ctrlvisivi': int_to_bool(art[9]),
            'file': int_to_bool(art[10]),
            'stato': int_to_bool(art[11]),
        }

    def get_codice_articolo(artnum):
        
