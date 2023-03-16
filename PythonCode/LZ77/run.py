import sys
sys.path.insert(0, 'PythonCode/LZ77/compressor')
sys.path.insert(1, 'PythonCode/LZ77/decompressor')

import decompressor.Decompressor as Decompressor
import compressor.Compressor as Compressor

from Decompressor import Decompressor
from Compressor import Compressor

def main() -> None:
    window_size = 25
    lookup_size = 6
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    message = "abababababa"

    compresor = Compressor(window_size, lookup_size, alphabet)
    mensaje_comprimido = compresor.compress(message, symb='_')
    print(mensaje_comprimido)

    decompresor = Decompressor(window_size, lookup_size, alphabet)
    mensaje_descomprimido = decompresor.decompress(
        mensaje_comprimido, symb='_')
    print(mensaje_descomprimido)

    return 0


main()
