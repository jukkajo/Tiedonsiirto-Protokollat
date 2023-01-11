
import sys
import re
import socket as s
from Latauspalkki import palkki
#from VirheTarkistin import palauta_viesti
from time import sleep

k = ["USER", "PASS", "QUIT", "PASV", "RETR", "LIST", "PWD"]
#kontrolliyhteyden portti
k_portti = 21 #21
host = "127.0.1.1"
#muut komennot / koodit
kom = ["220", "227", "331", "230", "550", "150", "257"]
wt="wt"

class Error(Exception):
    pass

def kommunikointi(soketti):

    puskuri = soketti.recv(1024)
    
    if kom[0] not in puskuri.decode():
        #print(puskuri)
        sys.exit("Palvelin ei vastaa")
    print(puskuri.decode()[4:].strip()) #220 ready tms
    try:
        kayttaja = input("Kayttaja: ")
        vastaa = k[0] + " " + kayttaja + "\r\n" # USER nimi \n
        soketti.send(str.encode(vastaa))
        
        vastaus = soketti.recv(1024)

        if kom[2] not in vastaus.decode():
            raise Error
        print(vastaus.decode()[4:].strip())
                    
        salasana = input("Salasana: ")
        soketti.send(str.encode(k[1] + " " + salasana + "\r\n"))
        vastaus2 = soketti.recv(1024)

        if kom[3] not in vastaus2.decode():
            raise Error    
        print(vastaus2.decode()[4:].strip())
        print("Kirjautuminen onnistui! Ohjelma valmiina komennoille, näet ne kirjoittamalla esim: 'h'")
            
    except Error:
        soketti.close()
        sys.exit("Kirjautuminen ei onnistunut")

    #kuunnellaan syötteitä käyttäjältä, kunnes antaa sopivia käskyjä
    while True:
        komento = kayttajan_syote()
        #kättely
            
        if k[6] in komento:
        
            soketti.send(str.encode(komento + "\r\n"))
            vastaus = soketti.recv(1024).decode()
            print(vastaus[4:])

                    
        elif k[2] in komento:
            soketti.send(str.encode(k[2] + " \r\n"))
            soketti.close()
            print("Yhteys suljettu")
            sys.exit()
            
        elif k[5] in komento:
            #pyydetään palvelinta kuuntelemaan ei de factoa data porttia
            pas_soketti = tilan_vaihto(soketti)
            
            print("Passiivisessa tilassa!")
            soketti.send(str.encode(komento + " \r\n"))
            #print(str.encode(komento + " \r\n"))
            
            pal_vast = soketti.recv(1024).decode()
            if kom[4] in pal_vast:
                #print(pal_vast)
                print("Antamaasi hakemistoa ei löytynyt!")
            elif kom[5] in pal_vast:
                #jos 150 palvelimelta, niin kuunnellaan passiivista väylää
                pas_vast = pas_soketti.recv(1024)

                if pas_vast:
                    #tulostetaan mitä hakemistossa
                    print(pas_vast.decode())
                else: 
                    print("Hakemisto on tyhjä!")
            print("Poistutaan passiivisesta tilasta")
            pas_soketti.close()

        elif k[4] in komento:
            
            dat_sok = tilan_vaihto(soketti)
            
            soketti.send(str.encode(komento + " \r\n"))
            #print("Lähetimme: ", str.encode(komento + " \r\n"))
            #soketti.send(str.encode(pal_vast + " \n"))
            p_vast = dat_sok.recv(1024).decode()
            #print("P_vast: ", p_vast)
            #550 kom4
            if kom[5] in p_vast:
                pa_vast = dat_sok.recv(1024).decode()
                
                o_polku = p_vast[p_vast.rfind('/') + 1:p_vast.rfind('"')]
                
                tiedosto = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), o_polku), wt)
                # tiedosto = open()
                print("Tallennetaan tiedostoa...")
                tiedosto.write(pa_vast)
                
                tiedosto.close()
                print("Tiedosto noudettu!")
                    
            elif kom[4] in p_vast:
                #print(p_vast)
                print("Antamaasi tiedostoa ei löytynyt!")
            else:
                print("Palvelin ei toimi oletetusti. Vastasi siis: ", p_vast)
            print("Poistutaan passiivisesta tilasta")
            dat_sok.close()
            
#tilanvaihto aktiivista passiiviin
def tilan_vaihto(soketti):
    soketti.send(str.encode(k[3] + " \r\n"))
    #print(str.encode(k[3] + " \n"))
    
    while True:
        vastaus = soketti.recv(1024).decode()

        if kom[1] in vastaus:
            print("vastaus: ",vastaus)
            break
        
    mjono = vastaus[vastaus.find('(') + 1:vastaus.find(')')]
    t = mjono.split(',') 
    data_osoite = t[0] + '.' + t[1] + '.' + t[2] + '.' + t[3]
    data_portti = (int(t[4]) * 256) + int(t[5])
    soketti_pas = s.socket(s.AF_INET, s.SOCK_STREAM)
    print("Yhdistämme osoitteeseen: ", data_osoite, ", portin: ", data_portti, " kautta.")
    soketti_pas.connect((data_osoite, data_portti))
    return soketti_pas
    
    
def testaa_s(s,luku):
    t = False
    merkit = ""
   # merkit2 = "^LIST( \/([A-z0-9-_+]+\/)*)?$"
 
    #LIST
    if luku == 1:
        merkit = "^LIST( \/([A-z0-9-_+]+\/)*)?$"

    #RETR
    elif luku == 2:
        merkit = "^RETR (\/([A-z0-9-_+]+\/)*)?([a-zA-Z0_9]+)?.*$"
        
    
    if re.search(merkit, s):
        t = True
           
    return t


def kayttajan_syote():

    syote = input()
    vastaa = ""

    if syote == "h" or syote == "H":
        print("Käytettävät komennot: ( QUIT, RETR <SP> <pathname>, LIST [<SP><path>], PWD ), esimerkit komennoista LIST ja RETR saat kirjoittamalla: 'esim'")
    elif syote == "esim":
        print("Esimerkit:\nLIST /mnt/c/FTP/ftp/\nRETR /mnt/c/FTP/ftp/testi.txt")
        
    elif k[2] in syote.upper():
        vastaa = k[2]
    
    elif k[5] in syote.upper():
        
        if len(syote) > (len(k[4]) + 1):
            luku = 1 
            if testaa_s(syote,luku) == True:
                vastaa = syote
            else:
                print("Komennossasi (LIST) kiellettyjä/ylimääräisiä merkkejä!")
        
        #vastaa = syote
            
    elif k[4] in syote.upper():
        
        if len(syote) > (len(k[4]) + 1):
            luku = 2
            if testaa_s(syote,luku) == True:
                vastaa = syote

            else:
                print("Komennossasi (RETR) kiellettyjä/ylimääräisiä merkkejä!")       

        #vastaa = syote
                
    elif k[6] in syote.upper():
        vastaa = k[6]
    
    else:
        print("Kirjoitit: ", syote, ", se ei vastaa käytettäviä komentoja: 'QUIT', 'RETR <SP> <pathname>', 'LIST [<SP><path>]', 'PWD', esimerkkejä saat kirjoittamalla: 'esim'")
        
    if vastaa != "": 
        print("Vastasimme: ", vastaa)
        
    return vastaa
    
if __name__ == "__main__":
    sy = input("Tämä on simppeli FTP-asiakasohjelma! \nYhdistetäänkö palvelimeen " + host + " portin " + str(k_portti) + "  kautta? (k / e)\n")
    if sy != "k" or sy != "K":
        print("Soketin alustus...")

        #tämä on täysin turha ja resursseja syövä, mutta tulipahan kokeiltua
        for i in range(20):
            sleep(0.05)
            palkki(i+1, 20, tila='Tila:', palkin_pituus=60, merkki="¤")

        soketti = s.socket(s.AF_INET, s.SOCK_STREAM)
        soketti.connect((host, k_portti))
        print("\nYhdistetty!")
        kommunikointi(soketti)
    
    else:
        print("Emme yhdistäneet!")
