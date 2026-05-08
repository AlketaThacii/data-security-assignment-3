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