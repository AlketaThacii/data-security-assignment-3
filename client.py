import socket
import base64

from Crypto.Cipher import DES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

hostname = " "
portno = 0000

try:
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socketi eshte gati i gjeneruar")

    mySocket.connect((hostname, portno))
    print("Lidhja eshte arritur me serverin")

except:
    print("Nuk mund te lidhet me serverin")
    exit()