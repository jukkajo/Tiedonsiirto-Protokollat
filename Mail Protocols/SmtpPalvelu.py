from threading import Thread as T

#port 25, host localhost
import socket
from Sposti import Sposti

class SmtpPalvelu(T):

    #"palvelin" soketin(ip) luonti
    soketti = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    portti = 25
    #host = "127.0.0.1"
    host = "localhost"
    mones = 0    
    #attribuuttien "sidonta"
    def __init__(self,inbox):
        T.__init__(self)
        self.inbox = inbox
        #nyt ei aliprosessit keskeytä threadia
        self.daemon = True
        self.start()
        
        
    
    #vastaanotettavat
    vast = ["HELO","MAIL FROM","RCPT TO","DATA", ".\r\n", "QUIT"]
    #                   L          V
    #lahetetttavat 
    lah = ["220 ","250 ","354 ","221 ","500 "]
    
    k = [" 2.1.0 OK"," 2.1.5 OK"," 2.0.0 OK"]
    
    #montako yhteyspyyntöä voidaan ottaa jonoon
    pyynnot = 2
    laskuri = 0
    
    def run(self):
        self.soketti.bind((self.host,self.portti))
        self.soketti.listen(self.pyynnot)
        #tässä vaiheessa soketti käytettävissä
        while True:
            print("Protokolla alustettu(smtp), kuunnellaan yhteyspyyntöjä!")
            #hyväksytään uusia liityntöjä
            (asiakassoketti, osoite) = self.soketti.accept()
            
            with asiakassoketti:
                sPosti = Sposti()
                print("smtp-yhteys osoitteen: ", osoite, " kanssa")
                #ilmoitetaan valmius
                valmius = self.lah[0] + " " + self.host + " smtp-palvelu valmiudessa"
                asiakassoketti.send(valmius.encode("utf-8"))
            
                while True:
                    #puskuri
                    lah_data = asiakassoketti.recv(1024)
                    if not lah_data:
                        break
                    vastaus = self.smtp_kommunikointi(lah_data, sPosti)
                    vastaus = vastaus.encode()
                    if self.vast[5] not in lah_data.decode():
                        #lähetetään yhteyden yli utf8:na
                        asiakassoketti.send(vastaus)
                    #jos QUIT, niin maili valmis inboksille    
                    else:
                        asiakassoketti.send(vastaus)
                        self.inbox.sailo_sposti(sPosti)
                        print("uusi sposti :", sPosti)
                        print("smtp-yhteys osoitteeseen: ", osoite, " suljetaan")
                        asiakassoketti.close()
                        self.mones = 0
                        break
                        
                

    #Viestin kasittely/kommunikointi:
   
    def smtp_kommunikointi(self, data, sposti):
        viesti = data.decode("utf-8")
        #print(viesti)
        v_u_case = viesti.upper()
        
        if self.vast[0] in v_u_case and self.mones == 0:
            print("Asiakas vastasi: ", self.vast[0])
            vastaus = self.lah[1] + "Hei " + self.host + " !"
            print("Vastasimme: ", vastaus)
            self.mones += 1
            
        elif self.vast[1] in v_u_case and self.mones == 1:
            tmp = viesti.split(" ")
            vastaanottaja = tmp[1]
            print("Asiakas vastasi: ", v_u_case)
            sposti.lisaa_vastaanottaja(vastaanottaja)
            vastaus = self.lah[1] + self.k[0]
            print("Vastasimme: ", vastaus)
            self.mones += 1
            
        elif self.vast[2] in v_u_case and self.mones == 2:
            self.mones += 1
            print("Asiakas vastasi: ", v_u_case)
            tmp = viesti.split(" ")
            lahettaja = tmp[2]
            sposti.lisaa_lahettaja(lahettaja)
            vastaus = self.lah[1] + self.k[1] #tämän jälkeen client voi lähettää dataa
            print("Vastasimme: ", vastaus)
            
        elif self.vast[3] in v_u_case:
            print("Asiakas vastasi: ", self.vast[3])
            vastaus = self.lah[2] + " Lähetä viesti; lopeta <CRLF>.<CRLF>"
            
        #elif v_u_case.endswith(self.vast[4]):
        elif self.vast[4] in v_u_case:
            #.\r\n
            #012345...n
            print("Asiakas vastasi s-postilla!")
            raja = len(viesti) - 13 
            sisalto = viesti[3:raja]
            sposti.lisaa_sisalto(sisalto)
            vastaus = self.lah[1] + self.k[2]
        else:
            vastaus = self.lah[4]
        
        return vastaus
