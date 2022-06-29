class Articoli:
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

    def get_with_ddt_number(ddtnum):
        articoli = query(f"SELECT * FROM testpython.cefart0f WHERE cearddtid = '{num}'")
        return get_articoli(articoli)

    def update_lavorazioni(artnum, taglio, punzonatura, saldatura, piegatura, foratura):
        taglio = bool_to_int(taglio)
        punzonatura = bool_to_int(punzonatura)
        saldatura = bool_to_int(saldatura)
        piegatura = bool_to_int(piegatura)
        foratura = bool_to_int(foratura)
        DB.update_field()
       

    def get_articolo(art):
        return {
            'id': int(art[0]),
            'idcertificazione': int(art[1]),
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

    def get_articoli(artlist):
        diclist = []
        for art in artlist:
            diclist.append(get_articolo(art))
        return diclist

    def get_article_and_insert_it(request, ddtnum):
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
        insert_article(
            ddt=ddtnum,
            filedic=" ",
            codice_interno=codice_interno,
            quantita=quantita,
            punzonatura=bool_to_int(punzonatura),
            taglio=bool_to_int(taglio),
            piegatura=bool_to_int(piegatura),
            foratura=bool_to_int(foratura),
            saldatura=bool_to_int(saldatura),
            controlli_visivi=bool_to_int(controlli_visivi),
            controlli_dimensionali=bool_to_int(controlli_dimensionali))

