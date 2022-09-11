from bitarray import BitArray
from abc import ABC

class RandomnessSource(ABC):
    def next(self) -> BitArray:
        raise NotImplementedError()