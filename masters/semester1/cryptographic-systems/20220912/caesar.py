#!/usr/bin/python3

def caesar(symbol, key, size, decrypt = False):
    symbol = ord(symbol) - ord("A")
    key = -key if decrypt else key    
    cipher = (symbol + key) % size
    return chr(cipher + ord("A"))

def tcaesar(symbols, key, size, decrypt = False):
    return ''.join(caesar(x, key, size, decrypt) for x in symbols)

if __name__ == "__main__":
    cyphertext = "LEZMVIJKPJKLUVEKJ"
    for i in range(26):
        print(i, tcaesar(cyphertext, i, 26, True))

