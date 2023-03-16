from typing import List
from initialization_of_search_buffer import ini_search_buffer
from manual_reproducible_extension import reproducible_extension

"""
    Function: Reproducible extensions inside the sliding window.
    Authors: Esteban Hernández Ramírez & Carlos Eduardo Álvarez Cabrera.
    Date: 13/06/2022

    Reference: "II. THE COMPRESSION ALGORITHM". A Universal Algorithm for Sequential Data Compression.
                IEEE TRANSACTIONS ON INFORMATION THEORY, MAY 1977. Jacob Ziv and Abraham Lempel.

    Description: Given a string, a symbol of the alphabet, the length of the window and the lookahead buffer size,
                 first, perform a padding at the beggining of the given string, composed by the given symbol of
                 length size of the window minus lookahead buffer size. slide the window over the given string,
                 calculating the manual reproducible extension for the substring inside the window at each time.

    Demo (usage): 
            > sliding_window_reproducible_extension('ABABCBCBAABCABe', '0', 8, 4)
            > [(3, 0, 'A'), (3, 0, 'B'), (2, 2, 'C'), (2, 3, 'A'), (3, 1, 'B'), (3, 0, 'C'), (1, 2, 'e')]
"""

def sliding_window_reproducible_extension(string: str, symb: str, n: int, l: int):
    reproducible_extensions: List = []

    pad_string: str = ini_search_buffer(symb, n-l, string)
    buffer: str = pad_string[: n]
    window_pos: int = n
    while window_pos - l < len(pad_string):
        pos, size = reproducible_extension(buffer, (n-l)-1)

        reproducible_extensions.append((pos, size, buffer[(n-l)+size]))
        size += 1

        if window_pos < len(pad_string):
            buffer = buffer[size : window_pos]
            buffer += pad_string[window_pos : window_pos+size]
        else:
            buffer = buffer[size :]

        window_pos += size
    return reproducible_extensions