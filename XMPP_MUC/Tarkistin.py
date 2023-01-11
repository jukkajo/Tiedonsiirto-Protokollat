#tarkistin mm syötteille

import re

def tarkista_numeerisuus(syote):
    try:
        t=int(syote)
        return True
    except:
        return False

#tarkastaa ipv4 osoitteen
def tarkista_regex_palvelin(palv):
    #regex_nimi = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
    regex_ip = "^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}$"
    #if re.search(regex_nimi, palv) or re.search(regex_ip, palv):
    if re.search(regex_ip, palv):
        return True
    else:
        return False
        
def tarkista_jid(jid):
   at='@'
   regex_jid = "^(?:([^@/<>'\"]+)@)?([^@/<>'\"]+)(?:/([^<>'\"]*))?$"
   if re.search(regex_jid, jid):
       if at in jid:   
           return True
   else:
       return False

def etsi_kiellettyja(mjono):
   if re.search("[~!#$%^&*()_+{}:/;\']", mjono):
       return False
   else:
       return True
