"""
    Function: Reproduce extension based on the given pos, size and char.
    Authors: Esteban Hernández Ramírez & Carlos Eduardo Álvarez Cabrera.
    Date: 15/06/2022

    Reference:

    Description: Given the description of the reproducible extension: pos, size and char, append it
                 to the recovered string of the process of decodification.

    Demo (usage): 
            > reproduce_extension('aababa', 3, 2, 'c')
            > abc
"""

def reproduce_extension(string: str, pos: int, size: int, char: chr):
    extension = ''
    for i in range(pos, pos+size):
        string += string[i]
        extension += string[i]
    return extension + char