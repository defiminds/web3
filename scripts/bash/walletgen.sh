#!/bin/bash

echo "Gerando nova carteira Ethereum..."

# Gera a chave privada usando openssl
openssl ecparam -name secp256k1 -genkey -noout | openssl ec -text -noout > private_key.txt

# Extrai a chave pública a partir da chave privada gerada
openssl ec -in private_key.txt -pubout -out public_key.txt

# Formata a chave pública como um endereço Ethereum
address=$(cat public_key.txt | sed '1d;$d' | tr -d '[:space:]' | keccak-256sum -x -l | tr -d ' -' | tail -c 41)

# Imprime o resultado
echo "Endereço Ethereum: 0x$address"
echo "Chave privada salva em private_key.txt"
echo "Chave pública salva em public_key.txt"
