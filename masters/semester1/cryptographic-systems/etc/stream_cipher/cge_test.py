from cgencryptor import CGEncryptor
plaintext = "Was certainty remaining engrossed applauded sir how discovery. Settled opinion how enjoyed greater joy adapted too shy. Now properly surprise expenses interest nor replying she she. Bore tall nay many many time yet less. Doubtful for answered one fat indulged margaret sir shutters together. Ladies so in wholly around whence in at. Warmth he up giving oppose if. Impossible is dissimilar entreaties oh on terminated. Earnest studied article country ten respect showing had. But required offering him elegance son improved informed."
MODULO = 10
for A in range(MODULO):
    for B in range(MODULO):
        for SEED in range(MODULO):
            cge = CGEncryptor(A, B, MODULO, SEED)
            ciphertext = cge.encrypt(plaintext, "utf-8")
            dplaintext = cge.decrypt(ciphertext, "utf-8")
            if dplaintext != plaintext:
                print(A, B, SEED, "is not possible to decrypt!")

