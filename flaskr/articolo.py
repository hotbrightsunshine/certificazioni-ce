from webbrowser import get
from db import DB
from util import *

class Articolo:
    # Ritorna l'articolo dato il suo ID 
    def get(art_num):
        q = DB.select_star("testpython.cefart0f", f"cearid={art_num} AND cearata=' '")
        return q[0]

    # Ritorna gli articoli dato il suo DDT
    def get_with_ddt_number(ddtnum):
        articoli = DB.select_star("testpython.cefart0f", f"cearddtid={ddtnum} AND cearata=' '")
        return articoli

    # Elimina un articolo
    def delete(artnum):
        DB.update_field("testpython.cefart0f", "cearata", "'r'", f"cearid={artnum}")

        # Elimina tutte le sue saldature
        sald = DB.select_star("testpython.cefsal0f", f"cesaarid={artnum}")
        saldids = []
        for s in sald:
            saldids.append(int(s['CESAID']))
        for s in saldids:
            DB.update_field("testpython.cefsal0f", "cesaata", "'r'", f"cesaid={s}")

        # Elimina tutti i suoi materiali
        mat = DB.select_star("testpython.cefori0f", f"ceoridar={artnum}")
        matids = []
        for m in mat:
            matids.append(int(m['CEORID']))
        for m in matids:
            Articolo.delete_materiale(m)

        # Elimina tutti i suoi ordini 
        ords = DB.select_star("testpython.cefoda0f", f"ceoaidar={artnum}")
        ordids = []
        for o in ords:
            ordids.append(int(o['CEOAID']))
        for o in ordids:
            Articolo.delete_ordine(o)

    # Aggiorna le lavorazioni di un articolo
    def update_lavorazioni(artnum, taglio, punzonatura, saldatura, piegatura, foratura):
        taglio = Util.bool_to_int(taglio)
        punzonatura = Util.bool_to_int(punzonatura)
        saldatura = Util.bool_to_int(saldatura)
        piegatura = Util.bool_to_int(piegatura)
        foratura = Util.bool_to_int(foratura)

        q = f"""UPDATE testpython.cefart0f
            SET cearpunz = {punzonatura},
                ceartagl = {taglio},
                cearfora = {foratura},
                cearpieg = {piegatura},
                cearsald = {saldatura}
            WHERE cearid = {artnum}
        """
        DB.execute(q)

        
    # Aggiorna i controlli di un articolo
    def update_controlli(artnum, controlli_dimensionali, controlli_visivi):
        controlli_dimensionali = Util.bool_to_int(controlli_dimensionali)
        controlli_visivi = Util.bool_to_int(controlli_visivi)
        DB.update_field("testpython.cefart0f", "cearctdi", controlli_dimensionali, f"cearid={artnum}")
        DB.update_field("testpython.cefart0f", "cearctvi", controlli_visivi, f"cearid={artnum}")

    # Traduce una lista di articoli in una lista di hashmap
    def get_list(artlist):
        diclist = []
        for art in artlist:
            diclist.append(Articolo.get(art))
        return diclist

    # Prende la richiesta POST e il numero DDT e inserisce nel database un record. (Andrebbe migliorato...)
    def get_and_insert(request, ddtnum):
        def it_or_false(req):
            if req in request.form:
                return True
            else:
                return False
        codice_interno = request.form['codice-interno']
        quantita = request.form['quantita']
        Articolo.insert(
            ddt=ddtnum,
            filedic=" ",
            codice_interno=codice_interno,
            quantita=quantita)

    # Inserisce all'interno del database l'articolo dati i suoi campi
    def insert(ddt, codice_interno, quantita, filedic=' '):
        q = f"""INSERT INTO testpython.cefart0f (cearddtid, cearcdpa, cearqty, cearfile, cearata)
         VALUES ( '{ddt}', '{codice_interno}', {quantita}, '{filedic}', ' ')"""
        DB.execute(q)

    # Aggiorna i materiali con certificato di collaudo di un articolo
    def add_materiale_cert_collaudo(artnum, colata, certcollaudo, datacollaudo, tipo_materiale, dop=None):
        DB.execute(f"""INSERT INTO testpython.cefori0f (ceoridar, ceordopnr, ceorcolnr, ceorcllnr, ceorclldt, ceororig, ceortpma) 
            VALUES ({artnum}, '{dop}', '{colata}', '{certcollaudo}', '{datacollaudo}', '2', '{tipo_materiale}')""")  

    # Aggiorna i materiali in conto lavorazione di un articolo
    def add_materiale_conto_lavorazione(artnum, codicecomponente, numerocolata, punzonatura, tipo_materiale):
        DB.execute(f"""INSERT INTO testpython.cefori0f (ceoridar, ceorcdpar, ceorcolnr, ceorpunnr, ceororig, ceortpma) VALUES (
                {artnum}, '{codicecomponente}', '{numerocolata}', '{punzonatura}', '1', '{tipo_materiale}')""")  
        
    # Controlla se manca il materiale d'apporto
    def is_apporto_mancante(artnum):
        sald = DB.select_field("cearsald", "testpython.cefart0f", f"cearid={artnum}")
        is_article_with_saldatura = False
        for record in sald:
            if int(record['CEARSALD']) == 1:
                is_article_with_saldatura = True

        if not is_article_with_saldatura:
            return False
        else:
            ori = DB.select_star("testpython.cefori0f", f"ceoridar={artnum} and ceortpma='A'")
            if len(ori) == 0:
                return True
            else:
                return False

    # Ritorna gli ordini di un articoli
    def get_orders_of(artnum):
        return DB.select_star("testpython.cefoda0f", f"ceoaidar={artnum} AND CEOAATA=' '")

    # Ritorna la somma degli ordini di un articolo
    def get_sum_of_orders(list_of_orders):
        sum = 0
        for order in list_of_orders:
            sum = sum + order['CEOAQTY']
        return sum

    # Inserisce un nuovo ordine
    def insert_order(artnum, numero_ordine, data_ordine, quantita_ordine):
        DB.execute(f"""INSERT INTO testpython.cefoda0f (ceoaidar, ceoanume, ceoadata, ceoaqty) VALUES
            ({artnum}, '{numero_ordine}', '{data_ordine}', '{quantita_ordine}')
        """)
    
    # Elimina un ordine
    def delete_ordine(ordnum):
        DB.update_field("testpython.cefoda0f", "ceoaata", "'r'", f"ceoaid='{ordnum}'")

    # Elimina un materiale
    def delete_materiale(matnum):
        DB.update_field("testpython.cefori0f", "ceorata", "'r'", f"ceorid='{matnum}'")


        

