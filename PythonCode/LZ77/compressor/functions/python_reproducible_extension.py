from typing import Tuple

"""
    Function: Reproducible extension.
    Authors: Esteban Hernández Ramírez & Carlos Eduardo Álvarez Cabrera.
    Date: 12/06/2022

    Reference: "II. THE COMPRESSION ALGORITHM". A Universal Algorithm for Sequential Data Compression.
                IEEE TRANSACTIONS ON INFORMATION THEORY, MAY 1977. Jacob Ziv and Abraham Lempel.

    Description: Given a search buffer, a lookahead buffer, the window and the lookahead buffer sizes, return 
                 a description of the reproducible extension, defined in the reference, as the ordered triple:
                 position of occurrence, length of the match and next symbol following the reproducible extension
                 of the reproducible extension. Functionality not programmed from scratch: with python methods.

    Demo (usage): 
            > reproducible_extension('abbaabb','baba', 11, 4)
            > (2, 2, 'b')
"""

def reproducible_extension(search: str, lookahead: str, n: int, Ls: int) -> Tuple:
    pos: int = -1
    size: int = 0
    char: chr = ''

    for prefixsize in range(1, min(n-Ls, len(lookahead))):
        prefix: str = lookahead[ : prefixsize]
        p: int = search.rfind(prefix, 0, ((n-Ls) + prefixsize - 1))
        if p >= 0:
            pos = p
            size = prefixsize
            char = lookahead[size]
        else:
            break

    return pos, size, char