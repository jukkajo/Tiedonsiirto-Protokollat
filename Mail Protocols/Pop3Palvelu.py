from threading import Thread as T
import os
import ssl
import socket

class Pop3Palvelu(T):

    portti = 110
    host = "localhost"
    yhteydet = 1
    saap = ["USER", "PASS", "LIST", "QUIT"]
    v = ["+OK send PASS", "+OK Welcome.", "+OK ", " viestit: \n", "+OK Näkemiin!", "-ERR error"]
    
    def __init__(self, inbox):
        T.__init__(self)
        self.daemon = True
        self.start()
        self.inbox = inbox

    #pop3 kommunikointi
    def run(self):
    
        soketti = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soketti.bind((self.host,self.portti))
        soketti.listen(self.yhteydet)
        
        #ssl-varmenne
        polku = os.path.dirname(os.path.abspath(__file__))
        konteksti= ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        konteksti.load_cert_chain(certfile=polku + "/palvelin.crt", keyfile=polku + "/palvelin.key")
        konteksti.load_verify_locations(cafile=polku + "/asiakas.crt")
        print("Pop3 valmis, kuunnellaan yhteyspyyntöjä!")
        
        while True:

            (conn, addr) = soketti.accept()
            wsoketti = konteksti.wrap_socket(conn, server_side=True)
            with wsoketti:
                print("Yhteyspyyntö osoitteesta: ", addr)
                wsoketti.send(str.encode("+OK POP3 palvelin valmiudessa <" + self.host + ">\n"))

                while True:
                    try:
                        puskuri = wsoketti.recv(1024)
                        if puskuri:
                            vastaa = self.pop3_kommunikointi(puskuri)
                            if self.saap[3] not in puskuri.decode().upper():
                                wsoketti.send(str.encode(vastaa))
                            else:
                                print("Yhteys osoitteeseem ", addr, " katkaistu")
                                wsoketti.close()
                                break
                    except ConnectionAbortedError:
                        print("Tunnistautuminen ei onnistunut(SSL) \n", "Yhteys osoitteeseem ", addr, " katkaistu")

                        wsoketti.close()
                        break

    def pop3_kommunikointi(self, puskuri):
        
        viesti = puskuri.decode("UTF-8")
        vi = viesti.upper()
        print(viesti)
        if self.saap[0] in vi:
            vastaa = self.v[0]
        elif self.saap[1] in vi:
            vastaa = self.v[1]
        elif self.saap[2] in vi:
            tmp = self.inbox.laske_postit()
            vastaa = str(self.v[2] + str(tmp) + self.v[3] + self.inbox.palauta_pop3_postit())
        elif self.saap[3] in vi:
            vastaa = self.v[4]
        else:
           vastaa = self.v[5]

        return vastaa + "\n"
