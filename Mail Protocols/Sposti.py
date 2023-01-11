from datetime import datetime as d

#sailoo s-postin tiedot
class Sposti:
    sisalto = ""
    vastaanottaja = ""
    lahettaja = ""
    aika = d.now()
    aika = str(aika)
    
    #uusi instanssi
    def __init__(self):
        pass
    
    def lisaa_sisalto(self, sisalto):
        self.sisalto = sisalto
    
    def lisaa_vastaanottaja(self, vastaanottaja):
        self.vastaanottaja = vastaanottaja
        
    def lisaa_lahettaja(self, lahettaja):
        self.lahettaja = lahettaja
    
    #palauttaa sposti olion m-jonona
    def __str__(self):
        
        return "(" + self.aika + ") " + self.lahettaja + "-> " + self.vastaanottaja + "/viesti: " + self.sisalto
