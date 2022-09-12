from caesar import caesar

plaintext = "IAMTIRED"
key = "NICENICE"

def vigenere(symbol, key):
    return caesar(symbol, ord(key) - ord("A"), 26)

def dvigenere(symbol, key):
    return caesar(symbol, 26 - ord(key) - ord("A"), 26)

def tvigenere(symbols, key, vigenere_lambda ):
   return ''.join(vigenere_lambda(symbols[i], key[i % len(key)]) for i in range(len(symbols))) 
   
ciphertext = tvigenere(plaintext, key, vigenere)
dplaintext = tvigenere(ciphertext, key, dvigenere)

print(plaintext, ciphertext, dplaintext)
