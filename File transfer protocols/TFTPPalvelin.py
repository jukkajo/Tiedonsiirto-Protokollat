from yhdista_sok import yhdista_sok
import PakettiGen as pgen
import select as sel
import os
from Latauspalkki import palkki
#parametrit
host = "127.0.0.1"
cmd_portti = 69
tied_portti = 6969

#data
tavu_lkm = 512
#muu
tavu_lkm2 = 600
tavu_lkm3 = 516


rt="rt"
wt="wt"
#opkoodit
opk = [1, 2, 3, 4, 5]
nt = bytes(opk[0])

#vastaanotto-prosessi
def RRQ_tapahtuma(tied, osoite):
    print("Vaihdetaan tiedonsiirron-porttiin...")
    soketti = yhdista_sok(host, tied_portti, "sido")
    tied_sisalto = b''
    
    ack_paketti = pgen.palauta_ACK((nt + nt))
    soketti.sendto(ack_paketti, osoite)
    y, b = 1, 1
    ack2 = pgen.palauta_ACK((nt + bytes([opk[0]]))) #ack 1
    ind = 0    
    while True:
    
        #timeoutin implementointi
        while True:
             #r_data = sel.select([soketti], e, r, b)
             r_data = sel.select([soketti], [], [], y)
             
             if r_data[0]:
                 while True:
                     data, osoite = soketti.recvfrom(tavu_lkm2)

                     if pgen.varmista_data(data, b) == True:
                         #print("Data-paketti (vastaanotettu) kunnossa!")
                         break
                     else:
                         print("Data-paketti oli virheellinen, uudelleen lähetetään viimeisin 'ack'")
                         soketti.sendto(ack2, osoite)

                 break
                 

             else:

                 if ind < 15:
                     print("Data-paketin lähetys keskeytyi, uudelleen lähetetään...")
                     soketti.sendto(ack2, osoite)
                     ind += 1
                 else:
                 
                     print("Ohjelma ei toimi odotetusti, keskeytetään")
                     break
        
        soketti.sendto(pgen.palauta_ACK(data[2:4]), osoite)
        tied_sisalto += data[4:]
        b += 1

        #mikäli tavuja < 512, paketti viimeinen
        if len(data) < tavu_lkm3:
            sis_data = tied_sisalto.decode()
   
            tied2 = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), tied), wt)
     
            tied2.write(sis_data)
            tied2.close()
            print("Tiedoston lukun onnistui!")
            break

#lähetys-prosessi        
def WRQ_tapahtuma(puskuri, osoite):
    print("Vaihdetaan tiedonsiirron-porttiin...")
    soketti = yhdista_sok(host, tied_portti, "sido")
    b, y, i = 1, 1, 0
    data = puskuri.encode()
    #osoite = puskuri
    
    #512 tavun paketteja
    for i in range(0, len(data), tavu_lkm):
           # tässä b = block
           paketti = pgen.palauta_DATA(data[i:i + tavu_lkm], b)
           soketti.sendto(paketti, osoite)
           while True:
               #readlist, writelist, exceptionlist, timeout
               r_data = sel.select([soketti], [], [], y)
 
               #eka tavu != tyhjä, niin aloitetaan
               if r_data[0]:
                   while True:
                       vastaus = soketti.recv(tavu_lkm2)
                       if pgen.varmista_ack(vastaus, b) == True:
                           break
                       else:
                           print("Ack-paketti oli virheellinen, uudelleen lähetetään viimeisin 'block'")
                           soketti.sendto(paketti, osoite)
                   break

               else:
                   soketti.sendto(paketti, osoite)
                   print("Ack-paketin lähetys keskeytyi, uudelleen lähetetään...")
                   

           
           b += 1
    palkki(i+1, len(data), tila='Tila:', palkin_pituus=60, merkki="¤")       
    print("\nTiedosto lähetetty onnistuneesti!")
    soketti.close()

        
def kaynnista():
    soketti = yhdista_sok(host, cmd_portti, "sido")
    print("Palvelin alustettu!")
    #tied_nimi = ""
    while True:
        puskuri, osoite = soketti.recvfrom(tavu_lkm2)
        if puskuri:
            tavu_2 = puskuri[:2]
            
            #tarkastetaan, mikä koodi tavussa 2 wrq tai rrq
            if tavu_2 == (nt + bytes([opk[0]])):
                #jos 

                tied_nimi = pgen.palauta_req_info(puskuri)

                try:
                    file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), tied_nimi), rt)
                #valmis poikkeus
                except FileNotFoundError:
                    print("Ei kyseistä tiedostoa, suljetaan soketti...")
                    soketti.close()
                    break
                #lähetys-prosessi
                WRQ_tapahtuma(file.read(), osoite)
                break
 
            elif tavu_2 == (nt + bytes([opk[1]])):
                print(puskuri)
                print(pgen.palauta_req_info(puskuri))
                #pri = pgen.palauta_req_info(puskuri)
                RRQ_tapahtuma(pgen.palauta_req_info(puskuri), osoite)
                break
    
