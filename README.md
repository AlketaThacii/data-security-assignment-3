# data-security-assignment-3

Ky projekt implementon nje aplikacion Client-Server ne Python duke perdorur TCP sockets.
Komunikimi mes klientit dhe serverit realizohet ne forme te kriptuar duke perdorur:

DES-CBC per enkriptimin e mesazheve
RSA Public Key Cryptography per mbrojtjen e celesit sekret DES

Serveri mbeshtet komunikim me disa kliente njekohesisht duke perdorur threads dhe implementon sistem privilegjesh:

admin
read-only

Komandat e Mbështetura
Perdorues Read-Only:
LIST
READ 
EXIT

Admin:
LIST
READ
WRITE
EXEC
EXIT

LIST - Shfaq te gjithe file-at ne server.
READ - Lexon permbajtjen e nje file-i.
WRITE- Shkruan tekst ne nje file.
EXEC (vetem admin) - Ekzekuton nje Python file ne server.
EXIT - Mbyll lidhjen me serverin.

---

## Menyra e funksionimit te RSA & DES bashke

Ky projekt perdor kombinimin e RSA dhe DES per te realizuar komunikim te sigurt klient-server.

Serveri gjeneron RSA Public Key dhe Private Key. Public Key i dergohet klientit permes TCP lidhjes. Klienti gjeneron nje DES secret key 64-bit dhe e enkripton ate duke perdorur RSA Public Key. DES key i enkriptuar dergohet te serveri, ku dekriptohet me RSA Private Key.

Pas ketij procesi, klienti dhe serveri posedojne te njejtin DES key sekret. Ky celes perdoret per enkriptimin dhe dekriptimin e te gjitha mesazheve gjate komunikimit duke perdorur DES-CBC.

RSA perdoret vetem per mbrojtjen dhe shkembimin e DES key, ndersa DES perdoret per enkriptimin e komunikimit sepse eshte me i shpejte per transferimin e te dhenave.

---

## Perdorimi i IV ne DES-CBC

Ne DES-CBC perdoret nje Initialization Vector (IV) prej 8 byte per cdo mesazh te enkriptuar.

IV gjenerohet ne menyre random para enkriptimit te mesazhit dhe bashkengjitet me ciphertext para dergimit. Gjate dekriptimit, serveri ose klienti e ndan IV nga ciphertext dhe e perdor per te rikrijuar plaintext-in origjinal.

Perdorimi i IV siguron qe edhe nese dergohet i njejti plaintext disa here, ciphertext-i do te jete i ndryshem cdo here, duke rritur sigurine e komunikimit dhe duke parandaluar zbulimin e modeleve ne te dhena.

