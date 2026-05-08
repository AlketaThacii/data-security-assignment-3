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

    def encrypt_des(message, des_key):
    iv = get_random_bytes(8)
    cipher = DES.new(des_key, DES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(message.encode("utf-8"), DES.block_size))
    return base64.b64encode(iv + encrypted)

def decrypt_des(encrypted_data, des_key):
    raw_data = base64.b64decode(encrypted_data)
    iv = raw_data[:8]
    ciphertext = raw_data[8:]
    cipher = DES.new(des_key, DES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), DES.block_size)
    return decrypted.decode("utf-8")

public_key_pem = mySocket.recv(4096)
public_key = RSA.import_key(public_key_pem)

des_key = get_random_bytes(8)

rsa_cipher = PKCS1_OAEP.new(public_key)
encrypted_des_key = rsa_cipher.encrypt(des_key)

mySocket.send(encrypted_des_key)

print("DES key u krijua dhe u dergua i enkriptuar te serveri.")

