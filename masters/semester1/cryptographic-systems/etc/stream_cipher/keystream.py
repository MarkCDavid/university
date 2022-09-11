from randomness_source import RandomnessSource

class Keystream:
    def __init__(self, randomness_source: RandomnessSource):
        self.randomness_source = randomness_source
        self.bitarray = None
        self.index = 0
    
    def encrypt(self, source_bit) -> int:
        if self.bitarray is None or self.index >= self.bitarray.length:
            self.bitarray = self.randomness_source.next()
            self.index = 0
        key_bit = self.bitarray.get(self.index)
        self.index += 1
        return source_bit ^ key_bit
