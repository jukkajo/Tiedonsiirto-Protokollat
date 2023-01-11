import socket
import sys

# "palvelin" käynnistettävä ennen tätä ohjelmaa

print("Tervetuloa smtp-asiakas-ohjelmaan, tällä voit lähettää s-postia!\n")
yhdista = input("Yhdistä palvelimeen antamalla 'Y'\n")

if yhdista == "y" or yhdista == "Y":

    varma = input("Varmasti? ('k' / 'e')\n")
    if varma == "k":
        
        #lahetettavat
        l = ["HELO","MAIL FROM","RCPT TO","DATA\r\n", ".\r\n", "QUIT"]
        lopetus=l[4] + l[4]
        #vastaanotettavat
        v = ["220","250","354","221","500"]
        
        #nämä pyydetään käyttäjältä
        lahettaja = input("Anna lähettäjä: \n")
        
        vastaanottaja = input("Anna vastaanottaja: \n")
        viesti = input("Anna viesti: \n")
        #soketin alustus ja TCP-yhteyden luonti
        asiakassoketti = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #palvelin
        host = "localhost"
        #host = "127.0.0.1"
        #host = socket.gethostname()
        portti = 25
        mones = 0 #monesko 250 viesti
            
        #kättelyn aloitus, kuunnellaan
        asiakassoketti.connect((host, portti))
        puskuri = asiakassoketti.recv(1024).decode("utf-8")
        if v[0] in puskuri:
            print("Palvelin vastasi: ", puskuri)
            asiakassoketti.send(l[0].encode("utf-8"))
            print("Vastasimme: ", l[0])
        
        while True:
            #tämä ei lien paras ratkaisu, mutta menköön
            asiakassoketti.send((l[1] + " " + host).encode("utf-8"))
            puskuri2 = asiakassoketti.recv(1024).decode("utf-8")
            vas = v[1]
            
            if vas in puskuri2 and mones == 0:
                mones += 1
                tmp = (l[1] + ":<" + lahettaja + ">")
                asiakassoketti.send(tmp.encode("utf-8"))
                print("Palvelin vastasi: ", puskuri2)
                print("Vastasimme: ", tmp)

            elif vas in puskuri2 and mones == 1:
                mones += 1
                print("Palvelin vastasi: ", puskuri2)
                tmp = (l[2] + ":<" + vastaanottaja + ">" + l[4])
                asiakassoketti.send(tmp.encode("utf-8"))
                print("Vastasimme: ", tmp)
                
            elif vas in puskuri2 and mones == 2:
                print("Palvelin vastasi: ", puskuri2)
                print("Vastasimme: ", l[3])
                asiakassoketti.send(l[3].encode("utf-8"))
                mones += 1
                    
            elif v[2] in puskuri2:
                print("Palvelin vastasi: ", v[2])
                v1, v2, v3 = (l[4] + viesti).encode("utf-8"), lopetus.encode("utf-8"), (l[5] + l[4]).encode("utf-8")
                asiakassoketti.send(v1)
                asiakassoketti.send(v2)
                asiakassoketti.send(v3)
                print("vastasimme: ", viesti)
                print("vastasimme: ", l[5])
                recvuusi = asiakassoketti.recv(1024)
                print("Palvelin vastasi: ", recvuusi.decode())
                mones = 0
                break


