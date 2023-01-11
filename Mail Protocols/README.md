# Mail Protocols

Threading implementoitu, palvelin kuuntelee siis yhteyspyyntöjä smtp, pop3 -ja imap-porteilta "samanaikaisesti".
Pop3 välinen kommunikointi ssl-varmennettu. Tulostuksessa näkynee kosmeettisia virheitä.

Sertifikaattien luomis-komennot ajettava projektin kansiossa "Ties323", olennaista sekin, että
myös "Common name"-kohtaan annetaan jälleen "Ties323"

ssl-sertifikaatit:

Asiakas:
$ openssl req -new -newkey rsa:2048 -days 3 -nodes -x509 -keyout asiakas.key -out asiakas.crt

Palvelin:
$ openssl req -new -newkey rsa:2048 -days 3 -nodes -x509 -keyout palvelin.key -out palvelin.crt


Palvelimen käynnistäminen voi vaatia root-oikeudet. Sekä asiakasohjelmat, että palvelin käynnistyy komennolla:

$ python3 "tiedostonnimi.formaatti"

esim.

$ python3 Palvelin.py



