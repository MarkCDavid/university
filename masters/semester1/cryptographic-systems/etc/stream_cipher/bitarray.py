class BitArray:

    def __init__(self, bits: int, length: int) -> None:
        self.bits = bits
        self.length = length

    @staticmethod
    def fromBytes(bytes: bytes) -> 'BitArray':
        return BitArray(int.from_bytes(bytes, "little"), len(bytes) * 8)

    @staticmethod
    def empty(length: int) -> 'BitArray':
        return BitArray(int.from_bytes(bytes(length + 7 // 8), "little"), length)

    def shr(self, count: int) -> 'BitArray':
        return BitArray(self.bits >> count, self.length - count)

    def __init__(self, bits: int, length: int) -> None:
        self.bits = bits
        self.length = length

    def get(self, index) -> int:
        assert index < self.length
        return (self.bits >> index) & 1

    def set(self, index, value) -> None:
        assert value == 0 or value == 1
        self._set(index) if value == 1 else self._unset(index)

    def bytes(self) -> bytes:
        assert self.length % 8 == 0
        _bytes = []
        for i in range(0, self.length, 8):
            byte = 0
            for j in range(8):
                byte |= (self.get(i + j) << j)
            _bytes.append(byte)
        return bytes(_bytes)

    def _set(self, index) -> None:
        assert index < self.length
        self.bits |= (1 << index)

    def _unset(self, index) -> None:
        assert index < self.length
        self.bits &= (~(1 << index))

    def __str__(self) -> str:
        result = ""
        for i in range(self.length):
            result += str(self.get(i))
        return result

    