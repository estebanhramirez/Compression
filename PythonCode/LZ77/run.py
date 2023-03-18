import os
from collections import defaultdict
import numpy as np
import math
import sys
sys.path.insert(0, 'PythonCode/LZ77/compressor')
sys.path.insert(1, 'PythonCode/LZ77/decompressor')

import decompressor.Decompressor as Decompressor
import compressor.Compressor as Compressor

from Decompressor import Decompressor
from Compressor import Compressor


def build_datasets(compresor, decompresor):
    path = 'data/TXTs/dummy.txt'
    dir_path = os.path.dirname(os.path.realpath(path))

    train_corpus_word = []
    train_corpus_tags = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            with open(dir_path+'/'+file, 'r') as f:
                txt = f.read()
                print(txt)
                mensaje_comprimido_train = compresor.compress(txt, symb='_')
                mensaje_descomprimido_train = decompresor.decompress(mensaje_comprimido_train, symb='_')
                train_corpus_word += mensaje_descomprimido_train
                train_corpus_tags += mensaje_comprimido_train
    lim = 100
    with open('data/WSJ_02-21.pos', 'w') as f:
        for block, word in zip(train_corpus_tags[:-lim], train_corpus_word[:-lim]):
            if block[2] == '\n':
                tag = '('+str(block[0])+','+str(block[1])+','+'\\n'+')'
                f.write('\\n'+'\t'+str(tag)+'\n')
            else:
                tag = '('+str(block[0])+','+str(block[1])+','+block[2]+')'
                f.write(word+'\t'+str(tag)+'\n')

    with open('data/WSJ_24.pos', 'w') as f:
        for block, word in zip(train_corpus_tags[-lim:], train_corpus_word[-lim:]):
            if block[2] == '\n':
                tag = '('+str(block[0])+','+str(block[1])+','+'\\n'+')'
                f.write('\\n'+'\t'+str(tag)+'\n')
            else:
                tag = '('+str(block[0])+','+str(block[1])+','+block[2]+')'
                f.write(word+'\t'+str(tag)+'\n')


def main():
    window_size = 200
    lookup_size = 50
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    compresor = Compressor(window_size, lookup_size, alphabet)
    decompresor = Decompressor(window_size, lookup_size, alphabet)

    build_datasets(compresor, decompresor)

    return 0


main()
