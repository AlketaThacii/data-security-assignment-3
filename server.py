//pjesa e pare..



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