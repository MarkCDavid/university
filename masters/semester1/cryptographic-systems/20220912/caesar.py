#!/usr/bin/python3

def caesar(symbol, key, size):
    symbol = ord(symbol) - ord("A")
    cipher = (symbol + key) % size
    return chr(cipher + ord("A"))

def tcaesar(symbols, key, size):
    return ''.join(caesar(x, key, size) for x in symbols)

cyphertext = "LEZMVIJKPJKLVVEKJ"
for i in range(26):
    print(i, tcaesar(cyphertext, i, 26))

print(tcaesar("UNIVERISTYSTUDENTS", 26 - 9, 26))

