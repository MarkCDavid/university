from bitarray import BitArray
from congruential_generator import CongruentialGenerator
from keystream import Keystream

class CGEncryptor:
    
    def __init__(self, a, b, modulo, seed) -> None:
        self.a = a
        self.b = b
        self.modulo = modulo
        self.seed = seed

    def encrypt(self, plaintext: str, encoding: str) -> BitArray:
        return self._passthrough(BitArray.fromBytes(plaintext.encode(encoding)))

    def decrypt(self, ciphertext: BitArray, encoding: str) -> str:
        return self._passthrough(ciphertext).bytes().decode(encoding)

    def _passthrough(self, source: BitArray) -> BitArray:
        keystream = Keystream(CongruentialGenerator(self.a, self.b, self.modulo, self.seed))
        target = BitArray.empty(source.length)
        for index in range(source.length):
            source_bit = source.get(index)
            target_bit = keystream.encrypt(source_bit)
            target.set(index, target_bit)

        return target
