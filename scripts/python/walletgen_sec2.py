import os
import sys
import getpass
import tempfile
import io
from Crypto.PublicKey import RSA

def generate_wallet():
    # gera uma chave RSA de 2048 bits
    key = RSA.generate(2048)

    # obtém a chave privada como um objeto Crypto RSAKey
    private_key = key.export_key()

    # obtém a chave pública como uma string hexadecial
    public_key = key.publickey().export_key().hex()

    return private_key, public_key

def main():
    while True:
        print("Selecione uma opção:")
        print("1. Gerar uma nova carteira")
        print("2. Sair")

        choice = input("Opção selecionada: ")

        if choice == "1":
            password = getpass.getpass(prompt="Insira uma senha para criptografar a chave privada: ")

            # gera uma nova carteira
            private_key, public_key = generate_wallet()

            # criptografa a chave privada com a senha fornecida
            cmd = f'openssl pkey -in <(echo "{private_key}") -aes256'
            encrypted_private_key_bytes = os.popen(cmd).read().encode()

            # lê a chave privada criptografada em um objeto de buffer de memória
            with io.BytesIO(encrypted_private_key_bytes) as buffer:
                encrypted_private_key = buffer.read()

            # exibe os resultados para o usuário
            print(f"Chave pública: {public_key}")

            # armazena a chave privada criptografada em uma variável confidencial
            private_key_buffer = io.BytesIO()
            private_key_buffer.write(encrypted_private_key)
            private_key_buffer.seek(0)
            encrypted_private_key_confidential = private_key_buffer.read()

            # remove o arquivo de chave privada original
            os.remove("private_key.pem")

        elif choice == "2":
            sys.exit()

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
