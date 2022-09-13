from string import ascii_uppercase as alphabet
plaintext = "AURIMASSAKALYS"
key = "RPWZEGDCVNBTXQAFHLMIOUYSKJ"

def substitution(plaintext, key, alphabet):
    return ''.join(key[alphabet.index(x)] for x in plaintext)

ciphertext = substitution(plaintext, key, alphabet)
print(ciphertext)
dplaintext = substitution(ciphertext, alphabet, key)
print(dplaintext)
