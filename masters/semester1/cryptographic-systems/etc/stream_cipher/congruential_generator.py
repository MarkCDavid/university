from typing import List
from bitarray import BitArray
from randomness_source import RandomnessSource

class CongruentialGenerator(RandomnessSource):
  def __init__(self, a: int, b: int, modulo: int, seed: int) -> None:
    self.a = a
    self.b = b
    self.modulo = modulo
    self.seed = seed

  def set_seed(self, seed) -> None:
    self.seed = seed

  def next(self) -> BitArray:
    self.next_seed()
    return BitArray(self.seed, ((self.modulo.bit_length() + 7) // 8) * 8)

  def next_seed(self) -> int:
    self.seed = (self.a * self.seed + self.b) % self.modulo
    return self.seed

  def next_seeds(self, count) -> List[int]:
    return [self.next_seed() for _ in range(count)]
