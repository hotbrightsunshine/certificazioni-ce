from webbrowser import get
from db import DB
from util import *

class Articolo:
    # Ritorna l'articolo dato il suo ID 
    def get(art_num):
        q = DB.select_star("testpython.cefart0f", f"cearid={art_num} AND cearata=' '")
        print(q)
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
        print ("SALDATURE: ", sald)
        saldids = []
        for s in sald:
            saldids.append(int(s['CESAID']))
        for s in saldids:
            DB.update_field("testpython.cefsal0f", "cesaata", "'r'", f"cesaid={s}")

        # Elimina tutti i suoi materiali
        mat = DB.select_star("testpython.cefori0f", f"ceoridar={artnum}")
        print ("MATERIALI: ", mat)
        matids = []
        for m in mat:
            matids.append(int(m['CEORID']))
        print("ID MATERIALI: ", matids)
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
        DB.update_field("testpython.cefart0f", "cearpunz", f"'{punzonatura}'", f"cearid={artnum}")
        DB.update_field("testpython.cefart0f", "ceartagl", f"'{taglio}'", f"cearid={artnum}")
        DB.update_field("testpython.cefart0f", "cearfora", f"'{foratura}'", f"cearid={artnum}")
        DB.update_field("testpython.cefart0f", "cearpieg", f"'{piegatura}'", f"cearid={artnum}")
        DB.update_field("testpython.cefart0f", "cearsald", f"'{saldatura}'", f"cearid={artnum}")

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

    # Inserisce all'interno del database l'articolo dati i suoi campi
    def insert(ddt, codice_interno, quantita, filedic, punzonatura, piegatura, taglio, foratura, saldatura, controlli_visivi, controlli_dimensionali):
        q = f"""INSERT INTO testpython.cefart0f (cearddtid, cearcdpa, cearqty, cearpunz, ceartagl, cearfora, cearpieg, cearsald, cearctdi, cearctvi, cearfile, cearata)
         VALUES ( '{ddt}', '{codice_interno}', {quantita}, {punzonatura}, {taglio}, {foratura}, {piegatura}, {saldatura}, {controlli_visivi}, {controlli_dimensionali}, ' ', ' ')"""
        DB.execute(q)

    # Aggiorna i materiali con certificato di collaudo di un articolo
    def update_materiale_collaudo(artnum, colata, certcollaudo, datacollaudo, tipo_materiale, dop=None, _id=None):
        if _id==None:
            DB.execute(f"""INSERT INTO testpython.cefori0f (ceoridar, ceordopnr, ceorcolnr, ceorcllnr, ceorclldt, ceororig, ceortpma) 
                VALUES ({artnum}, '{dop}', '{colata}', '{certcollaudo}', '{datacollaudo}', '2', '{tipo_materiale}')""")  
        else:
            DB.update_field("testpython.cefori0f", "ceorcolnr", f"'{colata}'", f"ceorid={_id}")
            DB.update_field("testpython.cefori0f", "ceoridar", f"{artnum}", f"ceorid={_id}")
            DB.update_field("testpython.cefori0f", "ceorcllnr", f"'{certcollaudo}'", f"ceorid={_id}")
            DB.update_field("testpython.cefori0f", "ceorclldt", f"'{datacollaudo}'", f"ceorid={_id}")

    # Aggiorna i materiali in conto lavorazione di un articolo
    def update_materiale_conto_lavorazione(artnum, codicecomponente, numerocolata, punzonatura, tipo_materiale, dop=None, _id=None):
        if _id==None:
            DB.execute(f"""INSERT INTO testpython.cefori0f (ceoridar, ceorcdpar, ceorcolnr, ceorpunnr, ceororig, ceortpma) VALUES (
                    {artnum}, '{codicecomponente}', '{numerocolata}', '{punzonatura}', '1', '{tipo_materiale}')""")  
        else:
            DB.update_field("testpython.cefori0f", "ceorcolnr", f"'{numerocolata}'", f"ceorid={_id}")
            DB.update_field("testpython.cefori0f", "ceoridar", f"{artnum}", f"ceorid={_id}")
            DB.update_field("testpython.cefori0f", "ceorpunnr", f"'{punzonatura}'", f"ceorid={_id}")
            DB.update_field("testpython.cefori0f", "ceorcdpar", f"'{codicecomponente}'", f"ceorid={_id}")
        
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
    
    # Controlla se gli ordini di un articolo sono troppi
    def are_troppi_ordini(artnum):
        #se la quantita totale degli articoli è maggiore della quantità dell'articolo > False | True
        ordlist = DB.select_star("testpython.cefoda0f", f"ceoaidar={artnum} AND CEOAATA=' '")
        sum = Articolo.get_sum_of_orders(ordlist)
        totqty = Articolo.get(artnum)['CEARQTY']
        totqty = int(totqty)
        if sum > totqty:
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
    
    # Ritorna il massimo numero di ordini
    def get_max_ordini(artnum):
        sum_orders = Articolo.get_sum_of_orders(Articolo.get_orders_of(artnum))
        art_qty = DB.select_field("cearqty", "testpython.cefart0f", f"cearid={artnum}")
        print(art_qty)
        max_try = int(art_qty[0]['CEARQTY']) - sum_orders
        if max_try <= 0:
            return 0
        return max_try

    # Controlla se il numero di ordini massimo è uguale al numero di ordini messi dall'utente
    def is_difference_zero(artnum):
        ordlist = DB.select_star("testpython.cefoda0f", f"ceoaidar={artnum}")
        sum = Articolo.get_sum_of_orders(ordlist)
        totqty = Articolo.get(artnum)['CEARQTY']
        totqty = int(totqty)
        return sum == totqty

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


        

