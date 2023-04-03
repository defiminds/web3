#!/usr/bin/perl

use strict;
use warnings;
use Digest::SHA3 qw(sha3_256_hex);

print "Gerando nova carteira Ethereum...\n";

# Gera a chave privada usando OpenSSL
my $private_key = `openssl ecparam -name secp256k1 -genkey -noout | openssl ec -text -noout`;

# Salva a chave privada em um arquivo
open my $fh, '>', 'private_key.pem' or die "Não foi possível criar o arquivo: $!";
print $fh $private_key;
close $fh;

# Extrai a chave pública a partir da chave privada gerada
my $public_key = `openssl ec -in private_key.pem -pubout`;

# Salva a chave pública em um arquivo
open $fh, '>', 'public_key.pem' or die "Não foi possível criar o arquivo: $!";
print $fh $public_key;
close $fh;

# Formata a chave pública como um endereço Ethereum
$public_key =~ s/.*pub:\s+\K(\w{130}).*/$1/s;
my $address = substr(sha3_256_hex(pack("H*", $public_key)), -40);

# Imprime o resultado
print "Endereço Ethereum: 0x$address\n";
print "Chave privada salva em private_key.pem\n";
print "Chave pública salva em public_key.pem\n";
