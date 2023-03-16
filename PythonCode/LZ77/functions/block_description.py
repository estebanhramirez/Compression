import math
import numpy as np

def d2r(radix, decnum, current):
    res = decnum % radix
    decnum = decnum // radix
    if decnum == 0:
        return str(res) + current
    else:
        return d2r(radix, decnum, str(res) + current)

def dec2radix(radix, decnum):
    return d2r(radix, decnum, '')

def d2a(alphabet, decnum, current):
    radix = len(alphabet)
    res = decnum % radix
    decnum = decnum // radix
    if decnum == 0:
        return alphabet[res] + current
    else:
        return d2a(alphabet, decnum, alphabet[res] + current)

def dec2alpha(alphabet, decnum):
    return d2a(alphabet, decnum, '')

def radix2dec(radix, rnum):
    dec = 0
    for i in range(0,len(rnum)):
        dec += int(rnum[len(rnum)-i-1])*(radix**i)
    return dec

def block(pos, size, char, n, l, alphabet):
    cd = dec2alpha(alphabet, pos).rjust(int(math.ceil(math.log(n-l) / math.log(len(alphabet)))), alphabet[0])
    cd += dec2alpha(alphabet, size).rjust(int(math.ceil(math.log(l) / math.log(len(alphabet)))), alphabet[0])
    cd += char
    return cd

def alpha2dec(alphabet, anum):
    radix = len(alphabet)
    dec = 0
    for i in range(0,len(anum)):
        dec += alphabet.index(anum[len(anum)-i-1])*(radix**i)
    return dec

def deblock(word, alpha, n, l):
    pblen = int(np.ceil(np.log(n-l) / np.log(len(alpha)))) #code length for positions
    lblen = int(np.ceil(np.log(l) / np.log(len(alpha)))) #code length for lengths

    pos = alpha2dec(alpha, word[0:pblen])
    size = alpha2dec(alpha, word[pblen:pblen+lblen])
    char = word[pblen+lblen]
    return pos, size, char