"""
    Function: Initialize search buffer (dictionary).
    Authors: Esteban Hernández Ramírez & Carlos Eduardo Álvarez Cabrera.
    Date: 13/06/2022

    Reference: "II. THE COMPRESSION ALGORITHM". A Universal Algorithm for Sequential Data Compression.
                IEEE TRANSACTIONS ON INFORMATION THEORY, MAY 1977. Jacob Ziv and Abraham Lempel.

    Description: Given a string, a symbol and a padding size, initialize a initial search buffer (dictionary) 
                 as a padding of length n-Ls of the given symbol at the beggining of the string.

    Demo (usage): 
            > ini_search_buffer('b', 5, 'aaa')
            > bbbbbaaa
"""

def ini_search_buffer(symb: int, padsize: int, cad: str) -> str:
    pad: str = symb
    for i in range(1, padsize):
        pad += symb
    return pad + cad