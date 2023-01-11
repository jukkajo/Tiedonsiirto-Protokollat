FTP-asiakas toteuttaa komennot: user, pass, quit, pasv, retr, list ja pwd.
Datan siirrossa käytetään passiivista tilaa ja palvelimen antamaa porttia/osoitetta.

TFTP-asiakkaan, sekä TFTP-palvelimen puolella Timeout ja viimeisimmän paketin uudelleen lähetys, mikäli vastaus ei validi (block:in, op-koodin tarkistus yms).
Lisätty latauspalkki visualisoimaan tiedonsiirron tilaa.

Kääntäminen terminaalissa:

FTP-asiakas:
$ python3 FTPAsiakas.py

TFTP-palvelin:
$ python3 main.py

TFTP-asiakas:
$ python3 TFTPAsiakas.py
