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