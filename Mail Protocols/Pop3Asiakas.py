
import os
import socket as s
import ssl

portti = 110
host = "localhost"
saap = ["+OK POP3", "OK send PASS", "OK Welcome", "viestit", "Näkemiin!"]
vast = ["user ", "pass ", "list ", "quit", " \n"]

def pop3_kommunikointi(puskuri):
    
    viesti = puskuri.decode("UTF-8")
    vastaa = ""
    if saap[0] in viesti:
        vastaa = vast[0] + kayttaja
    elif saap[1] in viesti:
        vastaa = vast[1] + salasana
    elif saap[2] in viesti:
        vastaa = vast[2]
    elif saap[3] in viesti:
        print(viesti)
        vastaa = vast[3]
        
    return vastaa + vast[4]
    

def hae_postit():
    
    #soketin alustus
    soketti = s.socket(s.AF_INET, s.SOCK_STREAM)

    #ssl-varmenne
    #etsitään sieltä, jonne tallensimme ennen tämän ohjelman käynnistystä
    polku = os.path.dirname(os.path.abspath(__file__))
    konteksti = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=polku + "/palvelin.crt")
    konteksti.load_cert_chain(certfile=polku + "/asiakas.crt", keyfile=polku + "/asiakas.key")
    ws = konteksti.wrap_socket(soketti, server_side=False, server_hostname="Ties323")
    ws.connect((host, portti)) #täytyi näkyjään oll double
    
    while True:
        puskuri = ws.recv(1024)
        if puskuri:
            if saap[4] in puskuri.decode():
                break
            ws.send(str.encode(pop3_kommunikointi(puskuri)))
            
if __name__ == "__main__":
    print("Tervetuloa pop3-asiakasohjelmaan!")
    kayttaja = input("Kayttaja: ")
    salasana = input("Salasana: ")
    hae_postit()
