#XMPP-chat GUI
#Author: Jukka Joutsalainen
import time
import tkinter as tk
import tkinter.font as font
from Tarkistin import tarkista_numeerisuus, tarkista_regex_palvelin, tarkista_jid, etsi_kiellettyja #TODO: luokka tästä
import socket
from PakettiGenXmpp import PakettiGenXmpp

ikkuna = tk.Tk()
ikkuna.title("XMPP-Chat")

#ikkuna.geometry("400x440")

class varit:
    valkoinen = "AntiqueWhite1"
    punainen = "red"
    turkoosi = "turquoise"
    i_vari = "bisque2"
    vihrea = "DarkSeaGreen2"
    musta = "black"
    harmaa ="grey81"
    valkoinen2 = "white"
    

#säilöö mm. guin/käyttäjän manageroiman datan
class Sov:
    v=varit()
    def __init__(self):
        self.palvelin = ""
        #oletuksena, näin yleensä, voi olla muukin
        self.portti = 5222
        self.knimi = ""
        self.ssana = ""
        self.viesti = ""
        self.jid = ""
        self.interaktiivinen = False
        self.rekisteroi = True
        self.kirjaudu = True
        self.kirjautunut = None
        self.viesti = ""
        self.kontaktit = []
        self.e_svars=self.gen_s_var()#entryt
        #label virheilmoitusten generointiin
        self.viesti_id = 0
        self.virhe_label = {}
        self.txt_boxit = {}
        self.soketti = None
        self.timeout = 3 # tämä varmaan riittänee
        self.tavut = 2048
        self.nollatavu = bytes(1)
        self.viestikentan_txt = ""
        self.viestikentta = None
        self.scrollbar = None
        self.rivinumero = 0 
        
    def rekisteroi_vai_kirjaudu(self):
        luku = var.get()
    
        if luku == 1:
            self.rekisteroi = True
            self.kirjaudu = False     
        if luku == 2:
            self.kirjaudu = True
            self.rekisteroi = False   
        
    def interakt_tila(self): 
        if var2.get() == 0:
            self.interaktiivinen = False
        if var2.get() == 1:
            self.interaktiivinen = True
        
    def yhdista(self):
        palv=self.e_svars[0].get()
        port=self.e_svars[1].get()
 
        if tarkista_regex_palvelin(palv) == True:
            self.virhe_label[0].configure(text="Ip-osoitteiden käyttöä ei ole vielä\nimplementoitu. Syötä Dns:n mukainen nimi.")
        else:            
            self.palvelin = palv
            if tarkista_numeerisuus(port) == True:
                self.portti = port
                self.virhe_label[0].configure(text="")#tämä saattaa olla turha tässä
                #kaikki kunnossa-> alustetaan soketti
                self.soketti = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #yritetään yhdistää jos palvelin olisi validi jne.
                try:
                    self.soketti.connect((self.palvelin, self.portti))
                    self.virhe_label[0].configure(text="Yhdistetty") 
                except:
                    self.virhe_label[0].configure(text="Yhdistäminen ei onnistunut,\nonhan palvelimen nimi oikein?\nPorttina yleensä: 5222") 
            
            else:
                self.virhe_label[0].configure(text="Portin oltava numero, muotoa: 5222")
            
            
    def gen_s_var(self):
        t={}
        for i in range(5):
            t[i] = tk.StringVar()
        return t
    
    #rekisteröi uuden käyttäjän tai yrittää suorittaa kirjautumis-prosessin olemassa olevalle
    def kirjaudu_rek(self):
         s = self.e_svars[2].get()
         k = self.e_svars[3].get()
         
         if etsi_kiellettyja(s) == True and etsi_kiellettyja(k) == True:
             if len(s) >= 7 and len(k) >= 5:
                 self.ssana = s
                 self.knimi = k
                 self.virhe_label[0].configure(text="")

                 onko_kaytossa = "register"
                 v_2_oletus = '<iq type="result"'
                 tyhja = ""
                 iq = "</iq>"
                 res = 'type="result"'
                 
                 if self.rekisteroi == True:
                 #=======================================================================
                     #kättely 'greet' palvelimelle
                     greet_vastaus = self.greet_tapahtuma()
                     if not onko_kaytossa in greet_vastaus:
                         self.virhe_label[0].configure(text="Palvelin, johon yhdistimme,\nei tue rekisteröitymistä.")
                         return False
                     #luku = 1
                     viesti = pg.palauta_rekist_viesti(self.palvelin, self.knimi, 1, self.ssana)
                     self.laheta(viesti)
                     
                     if not v_2_oletus in self.vastaanota(tyhja):
                         self.virhe_label[0].configure(text="Rekisteröityminen ei onnistunut, nyt\nlienee ohjelma tai palvelin solmussa.")
                         return False
                      
                     viesti2 = pg.palauta_rekist_viesti(self.palvelin, self.knimi, 2, self.ssana)
                     self.laheta(viesti2)
                     palv_vastaus = self.vastaanota(iq)
                     if res in palv_vastaus:
                         self.virhe_label[0].configure(text="Rekisteröity, kirjaudu vielä.")
                         return True
                     else:
                         self.virhe_label[0].configure(text="Rekisteröityminen ei onnistunut.")
                         return False
                 #=======================================================================
                 if self.kirjaudu == True:
                     if self.kirjautunut == True:
                         self.virhe_label[0].configure(text="Olet jo kirjautuneena.")
                         #TODO: uloskirjautuminen
                         
                 else:
                     self.greet_tapahtuma()             
                     print(self.nollatavu)
             else:
                 self.virhe_label[0].configure(text="Salasanan pituuden oltava väh.\n7-merkkiä, käyttäjänimen väh.\n5-merkkiä.")
             
         else:
             self.virhe_label[0].configure(text="Salasanassa tai käyttäjänimessä\n kiellettyjä merkkejä!\nKiellettyjä: [~!#$%^&*()_+{}:;\']")
  
    def greet_tapahtuma(self):
        pg = PakettiGenXmpp()
        
        if self.soketti != None:
            
            greet_viesti = pg.palauta_greet_viesti(self.palvelin)
            self.laheta(greet_viesti)
            tunniste = "</stream:features>"
            return self.vastaanosta(tunniste)
            
        else:
            self.virhe_label[0].configure(text="Palvelimeen yhdistettävä ensin.")
         
    def laheta_msg(self):
            try:
                if self.soketti != None:
                    if self.interaktiivinen == True:

                        pg_olio = PakettiGenXmpp()
                        self.viesti_id = pg.palauta_iq_stanza_id(self.viesti_id)
                        if self.kirjautunut is not None and self.viesti != "":
                        
                            self.viesti = pg.palauta_kayttajan_viesti(self.knimi, self.jid, self.viesti_id, self.viesti)                       
                            self.virhe_label[0].configure(text="Lähetetty!")
                            self.viesti = self.txt_boxit[0].get("1.0","end-1c")
                            self.soketti.send(self.viesti)
                            
                            aika = time.time()
                            self.tulosta_viesti(aika, self.knimi, self.viesti)
                                               
                        elif self.kirjautunut is None:
                            self.virhe_label[0].configure(text="Kirjautuminen tulee suorittaa ennen\n viestin lähetystä")
                            
                        else:
                            self.virhe_label[0].configure(text="Viestikenttä ei voi olla tyhjä.")
                    else:
                        self.virhe_label[0].configure(text="Käyttääksesi Gui:ta, valitse checkbutton,\n interakt. ohjelma ei (vielä) tue\n komentorivi-argumentteja")
            #pysähtyy soketin puuttumiseen tai interakt. tilan puuttumisen ennen virheilmoitusta        
            except:
                self.virhe_label[0].configure(text="Unohditko yhdistää palvelimeen?")
                  
    
    def laheta(self,data):
        if len(data) > 0:
            self.soketti.send(data.encode("utf-8"))    
    

    def maarita_jid(self):
        j = self.e_svars[4].get()
        if tarkista_jid(j) == True:
            self.jid = j
            self.virhe_label[0].configure(text="Jid asetettu!")
        else:
            self.virhe_label[0].configure(text="Jid:in oltava muotoa: nimi@esim.com")
     
    def paata_sessio():
        exit_viesti = pg.palauta_exit_viesti().encode("utf-8")
        self.laheta(exit_viesti)
        self.soketti.shutdown(socket.SHUT_RDWR) #Tämä siksi, jos jollain meneillään olevalla prosessilla on 'kahva' sokettiin
        self.soketti.close()
        self.virhe_label[0].configure(text="Yhteys suljettu.")

    def nayta_kontaktit(self):
        print("kkkk")
    
    #"kuunnellaan" sokettia, tunnistetaan palvelimen vastauksia
    # Hyödyntää timeout:ia, sikäli, kun joutuu odottamaan palvelimen vastauksia
    def vastaanota(self, tunniste):
        alkuaika = time.time() #tähän vertaillaan
        self.soketti.settimeout(self.timeout)
        koko_data = b''
        try:
            while true:
                sok_data = self.soketti.recv(self.tavut)
                if len(sok_data) == 0:
                    return str(koko_data)
                    
                else: 
                    koko_data += sok_data

                    if isinstance(tunniste, bool):
                        mjono = '"id="' + str(self.viesti_id) + '"'
                        if mjono in str(koko_data):
                            return str(koko_data)
                    else:
                        if tunniste in str(koko_data):
                            return str(koko_data)
                    #jos 3s kulunut, palautetaan dataa, tai tyhjää      
                    if (time.time() - alkuaika) > self.timeout:
                        return str(koko_data)
        except socket.timeout:
            return str(koko_data)
        
    
    def tulosta_viesti(self, aika, lahettaja, viesti):
        self.viestikentta.config(state="normal")
        lahettaja = re.search(r'(.*?)@', lahettaja).group(1)
        viesti = "[%s] <%s> %s" % \
            (time.strftime("%H:%M:%S", localtime), msg_from, message)
        viesti += "\n"
        #self.virhe_label[1].configure(text=viesti) #ei voi olla näin
        self.rivinumero += 1
        paikka = f'{self.rivinumero}.0'
        self.viestikentta.insert(paikka, viesti)
        self.viestikentta.config(state="disabled")


v=varit()
ikkuna.configure(background=v.musta)
fontti = tk.font.Font(family="Haettenschweiler", size=13, weight="bold")
              
lev=11
leveydet = [int(2.4*lev), lev-2, int((lev*2 + lev/3)*1.30), int(lev/2), int(lev*2)]
lev_framet=[[320, 260], [500, 260], [320, 260], [500, 260]]
indeksit=[[0,0], [0,1], [1,0], [1,1]]

kor=1
 
#dictionaryt sov. ikkunan komponenteille
dict_painikkeet = {}
dict_labelit = {}
entryt = {}
framet = {}
radio_painikkeet = {}
r_nimet = ["Rekisteröi", "Kirjaudu", "Tila/interakt."]

sov_olio = Sov()
l_nimet = ["Palvelin",
           "Portti",
           "Keskustelu",
           "Viestikenttä",
           "Salasana",
           "Käyttäjänimi",
           "Määrittele JID",
           "Kontaktit"]
           
p_nimet = ["yhdista", "Ok", "Lähetä", "Ok", "Näytä"]


#framet[0] -> dict_labelit[0], dict_labelit[1], dict_painikkeet[0], dict_labelit[4]
#framet[1] -> dict_labelit[2], dict_labelit[3], radio_painikkeet[0], radio_painikkeet[1], dict_painikkeet[1]
#framet[2] -> dict_labelit[5], t_kentta, dict_painikkeet[2], dict_painikkeet[3]
#framet[3] -> dict_painikkeet[4], radio_painikkeet[2], dict_labelit[6]

var=tk.IntVar() #rbutton

var2=tk.IntVar() #checkbutton
var2.set(1)

#sekvenssit asemoinnille:
#
#  0 | 1   
# -------
#  2 | 3

#dict_labelit
s1=[0,0,1,2,3,3,2,3]
k1_xy=[[10,10],[10,45],[170,10],[95,10],[250,155],[250,190],[95,192],[60,40]]
#dict_painikkeet
s2=[0,3,2,2,3]
k2_xy=[[10,75], [392,215], [10,155], [195,220], [25,210]]
#radio_painikkeet
s3=[3,3,3]
k3_xy=[[250,10],[370,10],[250,125]]
#entryt
s4=[0,0,3,3,2]
k4_xy=[[int(lev*13+8),10],[int(lev*13+8),45],[395,155],[395,190],[int(lev*8)+7,223]]

for i in range(len(l_nimet)):
   
    if i < 4:
    
        framet[i] = tk.Frame(master=ikkuna,
                             borderwidth=1,
                             width=lev_framet[i][0],
                             height=lev_framet[i][1],
                             background=v.valkoinen)
  
        framet[i].grid(row=indeksit[i][0], column=indeksit[i][1], padx=3, pady=3)
       
      
    dict_labelit[i] = tk.Label(text=l_nimet[i],
                                  fg=v.punainen,
                                  bg=v.i_vari,
                                  width=lev,
                                  height=kor,
                                  master=framet[s1[i]])
                                  
    dict_labelit[i]["font"] = fontti
    dict_labelit[i].place(x=k1_xy[i][0], y=k1_xy[i][1])

sov_olio.txt_boxit[0] = tk.Text(master=framet[2], width=leveydet[2]+3, height=int(kor*6),background=v.valkoinen, fg=v.turkoosi)
sov_olio.txt_boxit[1] = tk.Text(master=framet[3], width=leveydet[4]+3, height=int(kor*7),background=v.valkoinen, fg=v.turkoosi)

sov_olio.virhe_label[0] = tk.Label(text="",
                                fg=v.punainen,
                                bg=v.valkoinen,
                                width=leveydet[0]+10,
                                height=kor*5+1,
                                master=framet[0])
"""                                
sov_olio.virhe_label[1] = tk.Label(text="",
                                bg=v.turkoosi,
                                width= int(leveydet[0]*2.3),
                                height=kor*12,
                                master=framet[1])
"""
framet[4] = tk.Frame(master=framet[1],
                             borderwidth=1,
                             width=15,
                             height=lev_framet[1][1]-15)
                                                           
#----                                                           
sov_olio.virhe_label[0].place(x=10, y=116)
#sov_olio.virhe_label[1].place(x=10, y=40)
framet[4].place(x=480, y=5)

sov_olio.viestikentta = tk.Text(framet[1], width=58, height=14,fg=v.punainen, bg=v.i_vari)
sov_olio.scrollbar = tk.Scrollbar(framet[4], orient='vertical', command=sov_olio.viestikentta.yview) 
sov_olio.viestikentta['yscrollcommand'] = sov_olio.scrollbar.set

sov_olio.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
sov_olio.viestikentta.place(x=5, y=5)

sov_olio.viestikentta.config(state="disabled")
#----     

#giffin framet
framelkm=48
gif_framet = [tk.PhotoImage(file="snak.gif",format = "gif -index %i" %(i)) for i in range(framelkm)]

#=================================================
def paivita(i):
    frame=gif_framet[i]
    i+=1
    #nollataan kun iteroitu loppuun
    if i == framelkm:
        i=0
    pyth_label.configure(image=frame)
    framet[0].after(48, paivita, i)
        
pyth_label = tk.Label(master=ikkuna)
pyth_label.place(x=3, y=237)
pyth_label.after(0, paivita, 0)
#=================================================

sov_olio.txt_boxit[0].place(x=10, y=40)
sov_olio.txt_boxit[1].place(x=25, y=75)

funklista = [sov_olio.yhdista, sov_olio.kirjaudu_rek, sov_olio.laheta_msg, sov_olio.maarita_jid, sov_olio.nayta_kontaktit]


for i in range(len(p_nimet)):
    dict_painikkeet[i] = tk.Button(fg=v.musta,
                                   bg=v.vihrea,
                                   width=leveydet[i],
                                   height=kor,
                                   text=p_nimet[i],
                                   master=framet[s2[i]],
                                   command=funklista[i])
                                   
    entryt[i] = tk.Entry(fg=v.turkoosi,
                         bg=v.valkoinen,
                         width=lev,
                         master=framet[s4[i]],
                         textvariable=sov_olio.e_svars[i])
    
    dict_painikkeet[i].place(x=k2_xy[i][0],y=k2_xy[i][1])                    
    entryt[i].place(x=k4_xy[i][0], y=k4_xy[i][1])
    
    if i < 3: #
        if i == 2:
            radio_painikkeet[i] = tk.Checkbutton(master=framet[s3[i]], text=r_nimet[i], variable=var2, background=v.turkoosi, width=lev, onvalue=1, offvalue=0, command=sov_olio.interakt_tila)
        else:
            radio_painikkeet[i] = tk.Radiobutton(master=framet[s3[i]], text=r_nimet[i], variable=var, value=i+1, background=v.turkoosi, width=lev, command = sov_olio.rekisteroi_vai_kirjaudu) 

        radio_painikkeet[i].place(x=k3_xy[i][0], y=k3_xy[i][1])


                                      
ikkuna.mainloop()
