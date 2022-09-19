

def f(key, block):
    return (key * block) % 2**32

plaintext = "Hello, World!".encode("utf-8")

def round(blockL, blockR, key):
    return (blockR, blockL ^ f(key, blockR))

def feistele(key, blocks):
    result = []
    for i in range(0, len(blocks), 2):
        blockL, blockR = blocks[i], blocks[i + 1]
        for _ in range(16):
            blockL, blockR = round(blockL, blockR, key)
        result.append(blockL)
        result.append(blockR)
    return result

def feisteld(key, blocks):
    result = []
    for i in range(len(blocks) -1 , 0, -2):
        blockR, blockL = blocks[i], blocks[i - 1]
        for _ in range(16):
            blockR, blockL = round(blockR, blockL, key)
        result.append(blockR)
        result.append(blockL)
    return list(reversed(result))

blocks = [int.from_bytes(plaintext[i:i+4], "little") for i in range(0, len(plaintext), 4)]

key = 1241

cypher_blocks = feistele(key, blocks)
decrypted_blocks = b''.join(x.to_bytes(4, "little") for x in feisteld(key, cypher_blocks))

print(plaintext.decode("utf-8"))
print(decrypted_blocks.decode("utf-8"))

