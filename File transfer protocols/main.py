from TFTPPalvelin import kaynnista
import sys
import struct

if __name__ == "__main__":
    print("Tämä on TFTP-palvelin, käytettävät komennot näet kirjoittamalla: 'h'")
    
    k = ["h","sulje","suljetaan","yhdista"]
    while True:
        komento = input("")
        
        if komento.upper() == k[0].upper():
            print("Komennot: 'yhdista', 'sulje'") 

        elif komento.upper() == k[3].upper():
            kaynnista()
            
        elif komento.upper() == k[1].upper():
                break
            
    print(k[2])
    sys.exit()
    
