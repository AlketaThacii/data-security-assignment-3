import socket
import os
import subprocess
import threading
import base64

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


hostname = "192.168.0.104"
portno = 8080

SERVER_FOLDER = "server_files"
if not os.path.exists(SERVER_FOLDER):
    os.makedirs(SERVER_FOLDER)
from Crypto.PublicKey import RSA

ADMIN_KEY = "NETWORKADMIN2026"

rsa_key = RSA.generate(2048)
private_key = rsa_key
public_key = rsa_key.publickey()


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

def process_command(client_name, role, command):
    parts = command.strip().split(" ", 2)

    if not parts or parts[0] == "":
        return "Komande e zbrazet."

    main_command = parts[0].upper()

    if main_command == "LIST":
        files = os.listdir(SERVER_FOLDER)
        return "File ne server:\n" + "\n".join(files) if files else "Folderi bosh."

    elif main_command == "READ":
        if len(parts) < 2:
            return "Perdorimi: READ emri_file.txt"

        filename = parts[1]
        filepath = os.path.join(SERVER_FOLDER, filename)

        if not os.path.exists(filepath):
            return "File nuk ekziston."

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            return "Permbajtja e file-it '{}':\n{}".format(filename, content)
        except Exception as e:
            return "Gabim gjate leximit: {}".format(str(e))
    elif main_command == "WRITE":
        if role != "admin":
            return "Nuk keni privilegje."

        if len(parts) < 3:
            return "Perdor: WRITE file.txt tekst"

        filename = parts[1]
        text = parts[2]
        filepath = os.path.join(SERVER_FOLDER, filename)

        try:
            with open(filepath, "a", encoding="utf-8") as f:
                f.write(text + "\n")
            return "Shkrimi u krye."
        except Exception as e:
            return "Gabim: {}".format(str(e))
        
        

//pjesa e dyte e serverside
//komanda excecute
elif main_command == "EXEC":
        if role != "admin":
            return "Nuk keni privilegje."

        if len(parts) < 2:
            return "Perdor: EXEC file.py"

        filename = parts[1]
        filepath = os.path.join(SERVER_FOLDER, filename)

        if not os.path.exists(filepath):
            return "File nuk ekziston."

        try:
            result = subprocess.run(
                ["python", filepath],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout + result.stderr
        except Exception as e:
            return "Gabim gjate ekzekutimit: {}".format(str(e))
    elif main_command == "EXIT":
        return "DISCONNECT"

    else:
        return "Komande e panjohur."


def handle_client(client, addr):
    print(f"Lidhje nga {addr}")

    try:
        #Serveri ia dergon klientit public key
        public_key_pem = public_key.export_key()
        client.send(public_key_pem)

        #Serveri pranon DES key te enkriptuar me RSA public key
        encrypted_des_key = client.recv(4096)

        rsa_cipher = PKCS1_OAEP.new(private_key)
        des_key = rsa_cipher.decrypt(encrypted_des_key)
        
        print("DES key u pranua dhe u dekriptua me sukses.")

        #Prano login data te enkriptuar me DES-CBC
        encrypted_login = client.recv(4096)
        login_data = decrypt_des(encrypted_login, des_key).strip()

        if "|" in login_data:
            client_name, secret_key = login_data.split("|", 1)
        else:
            client_name = login_data
            secret_key = ""

        role = "admin" if secret_key == ADMIN_KEY else "read-only"
        
        #Komunikimi vazhdon i enkriptuar
        while True:
            encrypted_msg = client.recv(4096)

            if not encrypted_msg:
                break

            msg = decrypt_des(encrypted_msg, des_key)
            print(f"[NOTIFIKIM] Klienti '{client_name}' me rolin '{role}' kerkoi komanden: {msg}")
            response = process_command(client_name, role, msg)

            if response == "DISCONNECT":
                client.send(encrypt_des("Po mbyllet lidhja", des_key))
                break

            client.send(encrypt_des(response, des_key))
            
    except Exception as e:
        print("Gabim me klientin:", e)

    finally:
        client.close()
        print(f"Lidhja u mbyll {addr}")


mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socketi eshte gjeneruar")

mySocket.bind((hostname, portno))
print("Socketi eshte i lidhur me IP Addressen {} dhe portin {}".format(hostname, portno))

mySocket.listen(5)
print("Serveri eshte ne pritje te perdoruesve...")

while True:
    client, addr = mySocket.accept()
    threading.Thread(target=handle_client, args=(client, addr)).start()