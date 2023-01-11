#import threading
from T_Siirto_Protokollat import yhdista_sok as sok
from T_Siirto_Protokollat.xmpp_chat import etsi_kiellettyja as ek
import PakettiGenXmpp as pg
import sqlite3

# ts. Multi-user-chat
class XmmppPalvelin:
    def __init__(self):
        self.portti = None
        self.host = ""
        self.sido = "sido"
        self.soketti = None
        self.rosterit = Rosterit.rosters
        
        self.jidit = {}
        #tietokantaanhan nämä laittaa pitäisi
        self.ssanat = {}
        #iq stanzan id
        self.id = 0
        self.yht = sqlite3.connect("xmpp_muc.db")
        
        
    
    def reagoi(self, olio):
        rosterit_olio = Rosterit()
        rosteri_olio = Rosteri()
        while True
            (yhteys, osoite) = olio.soketti.accept()
            #
            with yhteys:
                sok_data = str(yhteys.recv(1023))
            
                if sok_data:
            
                
                    #pg.palauta_roster_result(rosteri_lista)
                    #rosterin get pyyntö
                    if "set" in sok_data and "<query" in sok_data:
            
                    #rosterin set
                    elif "get" in sok_data and "<query" in sok_data:
                        #  testataa, josko vain 1 item, kuten oletettu
                        if sok_data.count("item") == 2:
                    
                        else:
                           laheta("<forbidden/>", yhteys)
            
                    #tavallinen viesti
                    elif "</message>" in sok_data:
                        #tarkasta lähettäjän ryhmä
                        #tarkasta subscription == vastaanottaja
                    
            
                    elif "<presence" in sok_data:
            
                    #exit:in viesti
                    elif "<stream" in sok_data
    #varmentaa käyttäjän
    def varmenna(self):
    
 
 
    def laheta(self,data, yht):
        if len(data) > 0:
            yht.send(data.encode("utf-8"))
            
    def sailo_tkantaan(self, data_mjono, taulu, attr_johon):
        kursori = self.yht.cursor()
        
    def hae_tkannasta():
        
def kaynnista():
    palvelin_olio = XmmppPalvelin()   
    palvelin_olio.portti = input("Anna portti, yleensä '5222' (IANA): ")
    palvelin_olio.host = input("Anna host: ")
    palvelin_olio.soketti = sok(palvelin_olio.host, palvelin_olio.portti, "sido")
    reagoi(palvelin_olio)

class Rosterit:
  

class Rosteri:
    def __init__(self):
        
        self.approved = {}
        self.ask  = {} #subscription pyyntäjen kohteet, malli jid
        self.jid = ""
        #käyttäjä päättää tämän
        self.nimi = ""
        self.subscription = {}
        self.group = {}
        

if __name__ == "__main__":
    print("Tämä on Xmpp:tä mukaileva MUC, tai sanotaan, ei kovin kelpo toteutus")
    kaynnista()
    
    
