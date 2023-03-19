import os
from collections import defaultdict
import numpy as np
import math
import string
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
                txt = txt.replace("\t", "\\t")
                txt = txt.replace("\n", "\\n")
                #txt = txt[:5000]
                txt = 'a'*10000
                for i in range(0, len(txt)-100, 100):
                    subtxt = txt[i:i+100]
                    mensaje_comprimido_train = compresor.compress(subtxt, symb='_')
                    mensaje_descomprimido_train = decompresor.decompress(mensaje_comprimido_train, symb='_')
                    train_corpus_word += mensaje_descomprimido_train + ['\n']
                    train_corpus_tags += mensaje_comprimido_train + ['\n']

    with open('data/WSJ_02-21.pos', 'w') as f:
        for block, word in zip(train_corpus_tags, train_corpus_word):
            if block == '\n' and word == '\n':
                f.write('\n')
            else:    
                tag = '('+str(block[0])+','+str(block[1])+','+block[2]+')'
                f.write(word+'~'+str(tag)+'\n')
    


    test_corpus_tags = []
    test_corpus_word = []
    testtxt = 'a'*600 # "mi nombre es esteban hernandez ramirez y esta es una prueba del compresor lz77 utlizando la metodologia de POS tagging que aprendi en el curso de NLP de coursera. Espero que esto me sirva para encontrar patrones interesantes en los datos y podemos modelos el algoritmo lz77 como una cadena de markov oculta donde los estados son los bloques de codigo y los emitidos son las cadenas de coincidencia encontradas por el algoritmo de comresion. In this thesis, we provide a mono-graphic review about how information theory is applied to lossless compression. For this end, some of the implementations of lossless compression in coding theory and their respective analysis are presented. Furthermore, the proofs, graphs, algorithms, and implementations in this thesis generalize some of the most important facts about binary encodings, that have been stated in the literature, to the general case of alphabets of arbitrary size. This naturally led us to a general definition of some of the main information measures in terms of codes. Finally, an application of lossless compression in machine learning is presented, for the classification of natural language, through the application of the LZ77 coding scheme to estimate some well known information measures derivatives in the literature, which are elaborated as a distance metric to compare languages with each other. The result of the classification is presented in the form of phylogenetic trees of natural language."
    mensaje_comprimido_train = compresor.compress(testtxt, symb='_')
    mensaje_descomprimido_train = decompresor.decompress(mensaje_comprimido_train, symb='_')
    test_corpus_word += mensaje_descomprimido_train
    test_corpus_tags += mensaje_comprimido_train
    with open('data/WSJ_24.pos', 'w') as f:
        for block, word in zip(test_corpus_tags, test_corpus_word):
            tag = '('+str(block[0])+','+str(block[1])+','+block[2]+')'
            f.write(word+'~'+str(tag)+'\n')

def main():
    window_size = 200
    lookup_size = 20
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    compresor = Compressor(window_size, lookup_size, alphabet)
    decompresor = Decompressor(window_size, lookup_size, alphabet)

    build_datasets(compresor, decompresor)

    return 0


main()
