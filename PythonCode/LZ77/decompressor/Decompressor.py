import sys
sys.path.insert(0, 'PythonCode\LZ77\functions')
sys.path.insert(1, 'PythonCode\LZ77\decompressor\functions')

from functions.block_description import deblock
from decompressor.functions.reproduction_of_extension import reproduce_extension

"""
    Function: LZ77 decompressor class.
    Authors: Esteban Hernández Ramírez & Carlos Eduardo Álvarez Cabrera.

    Reference: "II. THE COMPRESSION ALGORITHM". A Universal Algorithm for Sequential Data Compression.
                IEEE TRANSACTIONS ON INFORMATION THEORY, MAY 1977. Jacob Ziv and Abraham Lempel.

    Description: Define an LZ77 decompressor given its sliding window size, lookahead buffer size, and code 
                 alphabet. Perform decompression over any given string given the decodifier parameters, as described
                 in the reference. Its method 'decompress' returns the list of reproducible extensions.

    Demo (usage):
            > decompresor = Decompressor(10, 5, ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
            > mensaje_descomprimido = decompresor.decompress(['aah', 'aao', 'aal', 'aaa', 'aa ', 'aam', 'aau', 'aan', 'aad', 'aao', 'aa ', 'cbe', 'aas', 'cc ', 'aal', 'cbm', 'aap', 'cbl', 'aa ', 'aaz', 'aai', 'aav', 'bb1', 'aa9', 'aa7', 'aa7'], symb='_')
            > print(mensaje_descomprimido)
            # ['h', 'o', 'l', 'a', ' ', 'm', 'u', 'n', 'd', 'o', ' ', 'de', 's', 'de ', 'l', 'em', 'p', 'el', ' ', 'z', 'i', 'v', ' 1', '9', '7', '7']
"""

class Decompressor:

    def __init__(self, window_size, lookahead_size, alphabet):
        self.n = window_size
        self.l = lookahead_size
        self.alpha = alphabet

    def decompress(self, compressed_string: str, symb: str):
        decompressed_string = []
        buffer = symb*(self.n - self.l)
        for block in compressed_string:
            pos, size, char = deblock(block, self.alpha, self.n, self.l)
            decompressed_string.append(reproduce_extension(buffer, pos, size, char))
            buffer += decompressed_string[-1]
            buffer = buffer[size+1 :]
        return decompressed_string