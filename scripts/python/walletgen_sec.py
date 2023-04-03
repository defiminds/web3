import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from eth_keys import keys

# Desabilita o registro de mensagens de log
logging.disable(logging.CRITICAL)

def generate_wallets(quantity):
    wallets = []
    for i in range(quantity):
        private_key = keys.PrivateKey()
        address = private_key.public_key.to_checksum_address()
        wallets.append({'private_key': private_key, 'address': address})
    return wallets

def export_wallets(wallets, encrypt=False):
    wallet_data = []
    for wallet in wallets:
        wallet_data.append(f'Private key: {wallet["private_key"].hex()}')
        wallet_data.append(f'Address: {wallet["address"]}')
    
    output = '\n'.join(wallet_data)

    if encrypt:
        # Gera uma chave para a criptografia
        key = Fernet.generate_key()
        fernet = Fernet(key)

        # Criptografa a saída
        encrypted_output = fernet.encrypt(output.encode())
        
        # Grava a chave criptográfica no arquivo de cabeçalho
        header = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend()
        )
        header_data = header.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        # Grava a chave criptográfica e os dados criptografados no arquivo
        with open('encrypted_wallets.txt', 'wb') as f:
            f.write(header_data + b'\n')
            f.write(key + b'\n')
            f.write(encrypted_output)
    else:
        print(output)

# Pede a quantidade de carteiras a serem geradas
quantity = int(input('Quantidade de carteiras a serem geradas: '))

# Gera as carteiras
wallets = generate_wallets(quantity)

# Pergunta se o usuário deseja exportar os dados para um arquivo criptografado
encrypt = input('Exportar em arquivo criptografado? (s/n): ').lower() == 's'

# Exporta as carteiras
export_wallets(wallets, encrypt=encrypt)
