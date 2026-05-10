# data-security-assignment-3
Ky projekt implementon nje aplikacion Client-Server ne Python duke perdorur TCP sockets.

Komunikimi realizohet ne forme te kriptuar duke perdorur:
- DES-CBC per enkriptimin e mesazheve
- RSA Public Key Cryptography per mbrojtjen e celesit sekret DES

Serveri mbeshtet komunikim me disa kliente njekohesisht duke perdorur threads dhe implementon sistem privilegjesh:
- admin
- read-only

## Komandat e Mbështetura:
### Read-Only
- LIST
- READ
- EXIT

### Admin
- LIST
- READ
- WRITE
- EXEC
- EXIT

## Pershkrimi i komandave
- LIST — shfaq file-at ne server
- READ — lexon nje file
- WRITE — shkruan tekst ne file
- EXEC — ekzekuton nje Python file ne server
- EXIT — mbyll lidhjen
