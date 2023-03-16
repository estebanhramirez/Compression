from typing import List
from .initialization_of_search_buffer import ini_search_buffer
from .python_reproducible_extension import reproducible_extension

"""
    Function: Reproducible extensions inside the sliding window.
    Authors: Esteban Hernández Ramírez & Carlos Eduardo Álvarez Cabrera.
    Date: 13/06/2022

    Reference: "II. THE COMPRESSION ALGORITHM". A Universal Algorithm for Sequential Data Compression.
                IEEE TRANSACTIONS ON INFORMATION THEORY, MAY 1977. Jacob Ziv and Abraham Lempel.

    Description: Given a string, a symbol of the alphabet, the length of the window and the lookahead buffer size,
                 first, perform a padding at the beggining of the given string, composed by the given symbol of
                 length size of the window minus lookahead buffer size. slide the window over the given string,
                 calculating the python reproducible extension for the substring inside the window at each time.

    Demo (usage): 
            > sliding_window_reproducible_extension('ABABCBCBAABCABe', '0', 8, 4)
            > [(0, 0, 'A'), (0, 0, 'B'), (2, 2, 'C'), (2, 3, 'A'), (3, 1, 'B'), (0, 0, 'C'), (1, 2, 'e')]
"""

def sliding_window_reproducible_extension(string: str, symb: str, n: int, l: int):
    totcode: List = []
    pcad: str = ini_search_buffer(symb, n-l, string)
    wpos: int = 0
    while wpos < len(pcad)-(n-l):
        pos, size, char = reproducible_extension(pcad[wpos:wpos+n], pcad[wpos+(n-l):wpos+n], n, l)
        if pos >= 0:
            totcode.append((pos, size, char))
        else:
            totcode.append((0, 0, pcad[wpos+(n-l)]))
        wpos += max(1,size+1)
    return totcode