from yhdista_sok import yhdista_sok
import PakettiGen as pg
import select as sel
import os
from Latauspalkki import palkki
host = "127.0.0.1"
tavu_lkm1, tavu_lkm2, tavu_lkm3 = 600, 516, 512
portti = 69
k=["WRQ","RRQ"]

t_out = 1
int_data = 0
rt = "rt"
wt = "wt"
sido = "ei"

def laheta_tied(v_osoite, tied_nimi, paketti, soketti):
    print("Vaihdetaan tiedonsiirron-porttiin...")
    try:
        file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), tied_nimi), rt)
        soketti.sendto(paketti, v_osoite)

        while True:
            #timeoutin implementointi
            block = 1
            while True:
            #saapunut data
                saap_data = sel.select([soketti], [], [], t_out)

                if saap_data[0]:
                    while True:
                        data, osoite = soketti.recvfrom(tavu_lkm1)
                        v_osoite = osoite

                        if pg.varmista_ack(data, int_data) == True:
                            break
                        else:
                            soketti.sendto(paketti, v_osoite)
                            print("Ack(0) oli virheellinen, uud. lähetetään viimeisin paketti...")
                    break
                else:
                    print("Ack(0) / timed out, uud. lähetetään...")
                    soketti.sendto(paketti, v_osoite)

            dat = file.read().encode()

            for i in range(0, len(dat), tavu_lkm3):
                osa_tiedosto = pg.palauta_DATA(dat[i:i + tavu_lkm3], block)
                soketti.sendto(osa_tiedosto, osoite)
                
                #latauspalkki visualisoimaan tilaa
                palkki(i+1, len(dat), tila='Tila:', palkin_pituus=60, merkki="¤")
                
                while True:
                    saap_data = sel.select([soketti], [], [], t_out)

                    if saap_data[0]:
                        
                        while True:
                            #palvelimen vastaus
                            pal_v = soketti.recv(tavu_lkm1)
                            if pg.varmista_ack(pal_v, block) == True:
                                break
                            else:
                                soketti.sendto(osa_tiedosto, osoite)
                        break
                    else:
                        soketti.sendto(osa_tiedosto, osoite)

                block += 1

            print("\nTiedosto lähetetty onnistuneesti!")
            break
            
    except FileNotFoundError:
        print("Tiedostoa ei löydy, kirjoitithan sen oikein?")

def vastaanota_tied(v_osoite, tied_nimi, paketti, soketti):
    print("Vaihdetaan tiedonsiirron-porttiin...")
    dat = b''
    block = 1

    soketti.sendto(paketti, v_osoite)
    

    while True:

        while True:
             saap_data = sel.select([soketti], [], [], t_out)

             if saap_data[0]:
                 while True:
                     data, osoite = soketti.recvfrom(tavu_lkm1)
                     v_osoite = osoite

                     if pg.varmista_data(data, block) == True:
                         break
                     else:
                         print("Vastaanotettu paketti oli virheellinen, uud. lähetetään viimeisin paketti...")
                         soketti.sendto(paketti, v_osoite)
                 break
             else:
                 print(" paketti / timed out, uud. lähetetään...")
                 soketti.sendto(paketti, v_osoite)

        paketti = pg.palauta_ACK(data[2:4])
        soketti.sendto(paketti, v_osoite)
        dat += data[4:]
        block += 1

        if len(data) < tavu_lkm2:
            tied = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), tied_nimi), wt)
            tied.write(dat.decode())
            tied.close()
            print("Tiedosto vastaanotettu!")
            break

             
def laheta_wrq_rrq(komento,luku,soketti):
    tied_nimi = input("Anna tiedostonnimi: ")
    paketti = pg.palauta_RRQ_tai_WRQ(tied_nimi, komento)
    #viimeisin
    v_osoite  = (host,portti)
    
    soketti.sendto(paketti, v_osoite)

    if luku == 1:
        print("Aloitetaan lähetys-prosessi")
        laheta_tied(v_osoite, tied_nimi, paketti, soketti)
    else:
        vastaanota_tied(v_osoite, tied_nimi, paketti, soketti)
        
if __name__ == "__main__":
    soketti = yhdista_sok(host, portti, sido)
    print("Soketti alustettu, yhdistetty hostiin: ", host, " portin: ", portti, " kautta!")
        
    while True:
        komento = input("Anna 'rrq' pyytääksesi tiedostoa tai 'wrq' siirtääksesi tiedoston: ")
        
        if komento.upper() == k[0]:
            laheta_wrq_rrq(komento, 1, soketti)
 
        elif komento.upper() == k[1]:
            laheta_wrq_rrq(komento, 2, soketti)
        else:
            print("Väärä komento, oikeat: 'wrq' tai 'rrq'")
        
