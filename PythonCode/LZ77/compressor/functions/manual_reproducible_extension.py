from typing import Tuple, List

"""
    Function: Reproducible extension.
    Authors: Esteban Hernández Ramírez & Carlos Eduardo Álvarez Cabrera.
    Date: 12/06/2022

    Reference: "II. THE COMPRESSION ALGORITHM". A Universal Algorithm for Sequential Data Compression.
                IEEE TRANSACTIONS ON INFORMATION THEORY, MAY 1977. Jacob Ziv and Abraham Lempel.

    Description: Given a string and an integer index in it, return a description of the reproducible extension,
                 defined in the reference, as the ordered pair: position of occurrence and length of the match
                 of the reproducible extension. Functionality programmed from scratch: with while loops.

    Demo (usage): 
            > reproducible_extension('abbaabbbaba', 6)
            > (2, 2)
"""

def reproducible_extension(S: str, j: int) -> Tuple:
    extensions: List[Tuple] = []

    i: int = 0
    while i <= j:
        extension: int = 1
        while ((extension < len(S)-(j+1)) and (S[i : i+extension] == S[(j+1) : (j+1)+extension])):
            extension += 1

        extensions.append(((extension-1), i))
        i = i + 1

    longest_reproducible_extension: Tuple = max(extensions)

    pos: int = longest_reproducible_extension[1]
    size: int = longest_reproducible_extension[0]
    return (pos, size)