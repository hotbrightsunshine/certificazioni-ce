from db import DB
from util import *

class Articolo:
    def get_from_record(record):
        return {
            'id': int(record[0]),
            'idcertificazione': int(record[1]),
            'codice_interno': record[2],
            'quantita': int(record[3]),
            'punzonatura': Util.int_to_bool(record[4]),
            'foratura': Util.int_to_bool(record[5]),
            'piegatura': Util.int_to_bool(record[6]),
            'saldatura': Util.int_to_bool(record[7]),
            'ctrldimensionali': Util.int_to_bool(record[8]),
            'ctrlvisivi': Util.int_to_bool(record[9]),
            'file': Util.int_to_bool(record[10]),
            'stato': Util.int_to_bool(record[11]),
        }

    def get_with_ddt_number(ddtnum):
        articoli = DB.select_star("testpython.cefart0f", f"cearddtid={ddtnum}")
        return Articolo.get_list(articoli)

    def update_lavorazioni(artnum, taglio, punzonatura, saldatura, piegatura, foratura):
        taglio = Util.bool_to_int(taglio)
        punzonatura = Util.bool_to_int(punzonatura)
        saldatura = Util.bool_to_int(saldatura)
        piegatura = Util.bool_to_int(piegatura)
        foratura = Util.bool_to_int(foratura)
        DB.update_field()
       
    def get(art):
        return {
            'id': int(art[0]),
            'idcertificazione': int(art[1]),
            'codice_interno': art[2],
            'quantita': int(art[3]),
            'punzonatura': Util.int_to_bool(art[4]),
            'foratura': Util.int_to_bool(art[5]),
            'piegatura': Util.int_to_bool(art[6]),
            'saldatura': Util.int_to_bool(art[7]),
            'ctrldimensionali': Util.int_to_bool(art[8]),
            'ctrlvisivi': Util.int_to_bool(art[9]),
            'file': Util.int_to_bool(art[10]),
            'stato': Util.int_to_bool(art[11]),
        } 

    def get_list(artlist):
        diclist = []
        for art in artlist:
            diclist.append(Articolo.get(art))
        return diclist

    def get_and_insert(request, ddtnum):
        def it_or_false(req):
            if req in request.form:
                return True
            else:
                return False
        codice_interno = request.form['codice-interno']
        quantita = request.form['quantita']
        punzonatura = it_or_false('punzonatura')
        taglio = it_or_false('taglio')
        piegatura = it_or_false('piegatura')
        foratura = it_or_false('foratura')
        saldatura = it_or_false('saldatura')
        controlli_visivi = it_or_false('controlli-visivi')
        controlli_dimensionali = it_or_false('controlli-dimensionali')
        Articolo.insert(
            ddt=ddtnum,
            filedic=" ",
            codice_interno=codice_interno,
            quantita=quantita,
            punzonatura=Util.bool_to_int(punzonatura),
            taglio=Util.bool_to_int(taglio),
            piegatura=Util.bool_to_int(piegatura),
            foratura=Util.bool_to_int(foratura),
            saldatura=Util.bool_to_int(saldatura),
            controlli_visivi=Util.bool_to_int(controlli_visivi),
            controlli_dimensionali=Util.bool_to_int(controlli_dimensionali))

    def insert(ddt, codice_interno, quantita, filedic, punzonatura, piegatura, taglio, foratura, saldatura, controlli_visivi, controlli_dimensionali):
        q = f"INSERT INTO testpython.cefart0f (cearddtid, cearcdpa, cearqty, cearpunz, ceartagl, cearfora, cearpieg, cearsald, cearctdi, cearctvi, cearfile, cearata) VALUES ( '{ddt}', '{codice_interno}', {quantita}, {punzonatura}, {taglio}, {foratura}, {piegatura}, {saldatura}, {controlli_visivi}, {controlli_dimensionali}, ' ', ' ')"
        DB.execute(q)

