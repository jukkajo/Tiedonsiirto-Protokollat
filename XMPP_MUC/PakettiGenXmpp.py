class PakettiGenXmpp:
#=============================Asiakas=====================================
    def palauta_iq_stanza_id(viesti_id):
        viesti_id += 1
        return viesti_id

    #rekisteröinnin viesti
    def palauta_rekist_viesti(palvelin, knimi, luku, ssana):
        if luku == 1:
            viesti = """
            <iq xmlns="jabber:client" type="get" to="%s">
            <query xmlns="jabber:iq:register"/>
            </iq>
            """ % (palvelin)
            
        else:
            #TODO: muuta var:it yms
            viesti = """
            <iq xmlns="jabber:client" type="set" to="%s">
            <query xmlns="jabber:iq:register">
            <x xmlns="jabber:x:data" type="form">
            <field type="hidden" var="FORM_TYPE">
            <value>jabber:iq:register</value>
            </field>
            <field type="text-single" var="username">
            <value>%s</value>
            </field>
            <field type="text-private" var="password">
            <value>%s</value>
            </field>
            </x>
            </query>
            </iq>
            """ % (palvelin, knimi, ssana)

    def palauta_greet_viesti(palvelin):
        viesti = """
        <?xml version="1.0"?>
        <stream:stream xmlns:stream="http://etherx.jabber.org/streams" 
        version="1.0" xmlns="jabber:client" to="%s">""" % (palvelin)
        return viesti


    def palauta_kayttajan_viesti(knimi, jid, viesti_id, viesti):
        
        viesti = """
        <message to="%s" from="%s" type="chat" id="%s">  
        <body>%s</body></message>
         """%(knimi, jid, str(viesti_id), viesti)

    def palauta_exit_viesti():
        viesti = """
        </stream:stream>
        """
#==========================Palvelin======================================

    #tällä vastataan roster-get:iin
    #oikea rosteri etsittävä valmiiksi tälle funktiolle
    def palauta_roster_result(rosteri, iq_id):
        
        if rosteri.subscription[0]:
            viesti_osa1 = """
            <iq id="%s"
            to="%s"
            type='result'>
            <query xmlns='jabber:iq:roster' ver='ver7'>
            """%(iq_id, rosteri.jid)
            
            for i in range(len(rosteri.subscription)):
            
                tmp = """
                <item jid="%s"/>
                """%(rosteri.subscription[i])
                viesti_osa1 += tmp
            
            viesti_osa1 += """
            </query>
            </iq>
            """
            return viesti_osa1
            
        else:
            viesti = """ 
            <iq id="%s"
            to="%s"
            type='result'>
            <query xmlns='jabber:iq:roster' ver='ver9'/>
            </iq>
            """%(iq_id, rosteri.jid)

    
    
        
    

