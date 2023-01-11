from Inbox import Inbox
from SmtpPalvelu import SmtpPalvelu
from Pop3Palvelu import Pop3Palvelu
from ImapPalvelu import ImapPalvelu

if __name__ == "__main__":
    print("Tervetuloa palvelimelle, tätä käytetään s-postin välitykseen!\nTuetut Protokollat: SMTP, POP3, IMAP")
    box = Inbox()
    smtp = SmtpPalvelu(box)
    pop3 = Pop3Palvelu(box)
    imap = ImapPalvelu(box)

while True:
   pass
