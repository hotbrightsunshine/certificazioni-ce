from db import DB
from util import *

class Articolo:
    def get(art_num):
        art_num = int(art_num)
        p= DB.select_field("cearddtid, cearcdpa, cearqty", "testpython.cefart0f", f"cearid={art_num}")
        print(p[0].cearddtid)
        return {
            'id': art_num,
            'idcertificazione': DB.select_field("cearddtid", "cefart0f", f"cearid={art_num}"),
            'codice_interno': DB.select_field("cearcdpa", "cefart0f", f"cearid={art_num}"),
            'quantita': DB.select_field("cearqty", "cefart0f", f"cearid={art_num}"),
            'punzonatura': Util.int_to_bool(DB.select_field("cearpunz", "cefart0f", f"cearid={art_num}")),
            'foratura': Util.int_to_bool(DB.select_field("cearfora", "cefart0f", f"cearid={art_num}")),
            'piegatura': Util.int_to_bool(DB.select_field("cearpieg", "cefart0f", f"cearid={art_num}")),
            'saldatura': Util.int_to_bool(DB.select_field("cearsald", "cefart0f", f"cearid={art_num}")),
            'ctrldimensionali': Util.int_to_bool(DB.select_field("cearctdi", "cefart0f", f"cearid={art_num}")),
            'ctrlvisivi': Util.int_to_bool(DB.select_field("cearctvi", "cefart0f", f"cearid={art_num}")),
            'file': Util.int_to_bool(DB.select_field("cearfile", "cefart0f", f"cearid={art_num}")),
            'stato': Util.int_to_bool(DB.select_field("cearata", "cefart0f", f"cearid={art_num}")),
        }

    def get_with_ddt_number(ddtnum):
        articoli = DB.select_star("testpython.cefart0f", f"cearddtid={ddtnum}")
        return articoli

    def update_lavorazioni(artnum, taglio, punzonatura, saldatura, piegatura, foratura):
        taglio = Util.bool_to_int(taglio)
        punzonatura = Util.bool_to_int(punzonatura)
        saldatura = Util.bool_to_int(saldatura)
        piegatura = Util.bool_to_int(piegatura)
        foratura = Util.bool_to_int(foratura)
        DB.update_field("testpython.cefart0f", "cearpunz", f"'{punzonatura}'", f"cearid={artnum}")
        DB.update_field("testpython.cefart0f", "ceartagl", f"'{taglio}'", f"cearid={artnum}")
        DB.update_field("testpython.cefart0f", "cearfora", f"'{foratura}'", f"cearid={artnum}")
        DB.update_field("testpython.cefart0f", "cearpieg", f"'{piegatura}'", f"cearid={artnum}")
        DB.update_field("testpython.cefart0f", "cearsald", f"'{saldatura}'", f"cearid={artnum}")

    def update_controlli(artnum, controlli_dimensionali, controlli_visivi):
        controlli_dimensionali = Util.bool_to_int(controlli_dimensionali)
        controlli_visivi = Util.bool_to_int(controlli_visivi)
        DB.update_field("testpython.cefart0f", "cearctdi", controlli_dimensionali, f"cearid={artnum}")
        DB.update_field("testpython.cefart0f", "cearctvi", controlli_visivi, f"cearid={artnum}")

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

    def update_materiale_collaudo(artnum, colata, certcollaudo, datacollaudo, num_dop=None, data_dop=None, _id=None):
        if _id==None:
            DB.execute(f"INSERT INTO testpython.cefori0f (ceoridar) VALUES ({artnum})")

        

