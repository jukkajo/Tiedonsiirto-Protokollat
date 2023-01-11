import socket as s

portti = 143
host = "localhost"

#koodit
k = ["a001","a002","a006"]
#muut
m = ["OK", "IMAP", "login", "logout", "\r\n", "select inbox"]

def imap_kommunikointi(puskuri):
    viesti = puskuri.decode("utf-8")
    vastaa = ""
    print(viesti)    
    #palvelin aloittaa yhteyden jälkeen, "OK IMAP palvelu val..."
    if m[0] + " " + m[1] in viesti:
        vastaa = k[0] + " " + m[2] + " " + kayttaja + " " + salasana
    elif k[0] + " " + m[0] in viesti:
        
        vastaa = k[1] + " " + m[5]
    elif k[1] + " " + m[0] in viesti:
        vastaa = k[2] + " " + m[3]
        print(viesti)

    return vastaa + m[4]


def hae_postit():
    soketti = s.socket(s.AF_INET, s.SOCK_STREAM)
    try:
        soketti.connect((host, portti)) #nämäkin voisi melkein kysyä käyttäjältä
    except:
        print("Soketin yhdistäminen ei onnistunut!")

    while True:
        puskuri = soketti.recv(2048)
        if puskuri:

            if k[2] + " " + m[0] in puskuri.decode():
                break

            vastaa = imap_kommunikointi(puskuri)
            
            if not vastaa.isspace():
                soketti.send(str.encode(vastaa))


if __name__ == "__main__":
    print("Tervetuloa pop3-asiakasohjelmaan!")
    kayttaja = input("Kayttaja: ")
    salasana = input("Salasana: ")
    hae_postit()
