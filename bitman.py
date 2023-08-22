import numpy as np
import itertools
import struct

class BitManipulator:
    def LSB_is_set(self, n: int) -> int:
        return n & 1
    
    def set_LSB(self, n: int) -> int:
        return n | 1
    
    def clear_LSB(self, n: int) -> int:
        return n & 0xFE
    
    def check_bit(self, n: int, bit_idx: int) -> int:
        return n & (1 << bit_idx)
    
    def set_bit(self, n: int, bit_idx: int) -> int:
        return n | (1 << bit_idx)
    
    def write_sequence(self, data: bytes, n: np.array, st_idx = 0) -> np.array:
        if len(data) * 8 > len(n):
            raise Exception(f"Not enough space ({len(data) * 8} bits required > {len(n)} bits available)")
        if st_idx % 8 != 0:
            raise Exception("st_idx must be multiple of 8")

        for byte in data:
            for bit_idx in range(8):
                if self.check_bit(byte, 7 - bit_idx):
                    n[st_idx] = self.set_LSB(n[st_idx])
                else:
                    n[st_idx] = self.clear_LSB(n[st_idx])
                st_idx += 1
        return n, st_idx

    def read_sequence(self, n: np.array):
        for i in range(0, len(n), 8):
            byte = 0
            if i + 8 > len(n):
                break
            for bit_idx in range(8):
                if self.LSB_is_set(n[i + bit_idx]):
                    byte = self.set_bit(byte, 7 - bit_idx)
            yield byte

class BitmanIO():
    """
    Utility class to make processing easier
    """
    def __init__(self, bitman, image: np.array):
        self._bitman = bitman
        self._image = image
        self._reader = self._bitman.read_sequence(self._image)
        self._st_idx = 0

    def read(self, n: int) -> None:
        return bytes(itertools.islice(self._reader, n))
    
    def write(self, data: bytes) -> None:
        self._image, self._st_idx = self._bitman.write_sequence(data, self._image, self._st_idx)
    
    def get_image(self) -> np.array:
        return self._image

class NDArraySequenceManipulator:
    """
    N-Dimensional array sequence manipulator
    """

    def __init__(self):
        self.bitman = BitManipulator()

    def write_sequence(self, data: bytes, image: np.array, header=True) -> np.array:
        writer = BitmanIO(self.bitman, image.flatten())
        if header:
            writer.write(struct.pack('Q', len(data)))
        writer.write(data)
        return writer.get_image().reshape(image.shape)

    def write_max_sequence(self, data: bytes, image: np.array, header=True) -> np.array:
        repeat = self.get_max_sequence_length(image) // len(data)
        data = data * repeat
        return self.write_sequence(data, image, header)

    def read_sequence(self, image: np.array, header=True) -> bytes:
        if header:
            reader = BitmanIO(self.bitman, image.flatten())
            length, = struct.unpack('Q', reader.read(8))
            return reader.read(length)
        else:
            return bytes(self.bitman.read_sequence(image.flatten()))
    
    def get_max_sequence_length(self, image: np.array) -> int:
        return len(image.flatten()) // 8 - 1