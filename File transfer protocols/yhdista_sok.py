import socket as s

#def yhdista_sok(host, yhteydet, portti):
def yhdista_sok(host, portti, sido):
    soketti = s.socket(s.AF_INET, s.SOCK_DGRAM)
    soketti.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 4)
    si = "sido"
    if sido == si:
        print("soketti sidottu porttiin: ", portti, " ja hostiin: ", host)
        soketti.bind((host, portti))
        
    #soketti.listen(yhteydet)
    return soketti
