from threading import Thread as T
import random as ra
import socket as s

class ImapPalvelu(T):

    portti = 143
    host = "localhost"
    yhteydet = 1
    
    #=========================================================
    
    #muu kommunikointi
    v = ["logout", "login", "ok", "\n", "completed", "exists", "recent", "select", "inbox", "bad"]
    #koodit
    k = ["a001","a002","a006"]
   
    #flagit yms.
    f = "* FLAGS (\Answered \Flagged \Deleted \Seen \Draft)"
    r = "[READ-WRITE]"
    n = "No such command"

    def __init__(self, inbox):
        T.__init__(self)
        self.daemon = True
        self.start()
        self.inbox = inbox

    #soketin alustus, y-pyyntöjen kuuntelu jne.
    def run(self):
        soketti = s.socket(s.AF_INET, s.SOCK_STREAM)
        soketti.bind((self.host,self.portti))
        soketti.listen(self.yhteydet)
        
        print("Imap-protokolla valmiina, kuunnellaan yhteyspyyntöjä!")
        while True:

            (yhteys, osoite) = soketti.accept()
            with yhteys:
                print("Yhteyspyyntö(IMAP) osoitteesta: ", osoite)
                yhteys.send(str.encode("OK IMAP palvelu valmiina osoitteelle  <" + osoite[0] + ">" + self.v[3]))

                while True:
                    puskuri = yhteys.recv(1024)
                    if puskuri:
                        vastaa = self.pop3_kommunikointi(puskuri)

                        if not vastaa.isspace():
                            if self.k[2] + self.v[0] not in puskuri.decode().upper():
                                yhteys.send(str.encode(vastaa))
                            else:
                                print("Katkaistaan IMAP-yhteys osoitteeseen: ", osoite)
                                yhteys.close()
                                break

    
    # toteutetaan vain vaadittu
    # S: * 172 EXISTS
    # S: * 1 RECENT
    #...
    # S: * FLAGS (\Answered \Flagged \Deleted \Seen \Draft)
    #...
    # S: A142 OK [READ-WRITE] SELECT completed
    
    # random arpomaan simuloitavia, mahdollisia viestien määriä           
    def pop3_kommunikointi(self, puskuri):
        
        viesti = puskuri.decode()
        
        if self.k[0] + " " + self.v[1] in viesti:
            vastaa = self.k[0] + " " + self.v[2].upper() + " " + self.v[1].upper() + self.v[4]

        elif (self.k[1] + " " + self.v[7] + " " + self.v[8]) in viesti:
            # \ - merkkillä monelle riville
            vastaa = str(ra.randint(1,100)) + " " + self.v[5].upper() + " " + self.v[3] \
                    + " " + self.f + " " + self.v[3] \
                    + " * " + str(self.inbox.laske_postit()) + " " + self.v[6].upper() + " " + self.v[3] \
                    + " " + self.k[1] + " " + self.v[2].upper() + " " + self.f + " " + self.v[7].upper() + " " + self.v[4]
                    
        elif self.k[2] + " " + self.v[0] in viesti:
            vastaa = self.k[2] + " " + self.v[2].upper() + " " + self.v[0].upper() + " " + self.v[4]
        else:
            vastaa = viesti[0:4] + " " + self.v[9].upper() + " " + self.n
   
        return vastaa + self.v[3]
