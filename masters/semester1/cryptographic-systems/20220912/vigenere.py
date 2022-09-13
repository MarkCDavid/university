from caesar import caesar

plaintext = "VILNIUSGEDIMINASTECHNICALUNIVERSITY"
key = "AURIMASSAKALYSAURIMASSAKALYSAURIMASSAKALYS"

def vigenere(symbol, key, decrypt = False):
    return caesar(symbol, ord(key) - ord("A"), 26, decrypt)

def tvigenere(symbols, key, decrypt = False):
    return ''.join(vigenere(symbols[i], key[i], decrypt) for i in range(len(symbols))) 
   
ciphertext = tvigenere(plaintext, key)
dplaintext = tvigenere(ciphertext, key, True)

print(plaintext, ciphertext, dplaintext)
