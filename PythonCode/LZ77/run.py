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


def build_train_corpus(compresor, decompresor):
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
                txt = txt[:6000]
                for i in range(0, len(txt)-36, 36):
                    subtxt = txt[i:i+36]
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


def build_test_corpus(compresor, decompresor):
    test_corpus_tags = []
    test_corpus_word = []
    testtxt = "my name is esteban hernandez and i am a colombia applied mathematician and computer scientist who was born in girardot cundinamarca and currently has twenty two years old. for my thesis i worked on information theory and still working on it until now. how i can make something great soon. this is my dream. thanks for your time and have a great day. see you soon buddy."
    mensaje_comprimido_train = compresor.compress(testtxt, symb='_')
    mensaje_descomprimido_train = decompresor.decompress(mensaje_comprimido_train, symb='_')
    test_corpus_word += mensaje_descomprimido_train
    test_corpus_tags += mensaje_comprimido_train
    with open('data/WSJ_24.pos', 'w') as f:
        for block, word in zip(test_corpus_tags, test_corpus_word):
            tag = '('+str(block[0])+','+str(block[1])+','+block[2]+')'
            f.write(word+'~'+str(tag)+'\n')


def main():
    window_size = 10
    lookup_size = 5
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    compresor = Compressor(window_size, lookup_size, alphabet)
    decompresor = Decompressor(window_size, lookup_size, alphabet)

    build_train_corpus(compresor, decompresor)
    build_test_corpus(compresor, decompresor)

    text = ['(0,0,m)', '(0,0,y)', '--s--', '(0,0,n)', '(0,0,a)', '(0,0,x)', '(0,0,i)', '(0,0,s)', '(0,0,e)', '(3,1,t)', '(0,0,z)\n', '(0,0,a)\n', '(0,0,n)\n', '--s--', '(0,0,h)\n', '(0,0,e)\n', '(0,0,r)\n', '(1,1,b)\n', '(2,1,d)\n', '(0,0,e)\n', '(0,1,l)\n', '--s--', '(0,0,a)\n', '(0,0,n)\n', '(0,0,d)\n', '(0,1,d)\n', '(0,0,a)\n', '(0,0,m)\n', '(0,0,a)\n', '(0,0,c)\n', '(0,0,o)\n', '(0,0,l)\n', '(0,1,m)\n', '(0,0,b)\n', '(0,1,m)\n', '(0,0,a)\n', '--s--', '(0,0,y)\n', '(2,1,l)\n', '(0,0,i)\n', '(0,0,e)\n', '(0,0,d)\n', '--s--', '(0,0,m)\n', '(0,0,a)\n', '(0,0,t)\n', '(0,0,h)\n', '(0,0,e)\n', '(2,1,s)\n', '(0,0,c)\n', '(4,1,e)\n', '(0,0,n)\n', '--s--', '(0,0,\ufeff)\n', '(0,0,c)\n', '(0,0,o)\n', '(0,0,m)\n', '(1,1,B)\n', '(0,0,u)\n', '(0,0,t)\n', '(0,0,e)\n', '(0,0,r)\n', '--s--', '(0,0,s)\n', '(0,0,c)\n', '(0,0,i)\n', '(0,0,e)\n', '(0,0,n)\n', '(0,0,t)\n', '(1,1,s)\n', '(0,0,t)\n', '(0,0,w)\n', '(0,0,h)\n', '(0,0,o)\n', '(4,1,k)\n', '(0,0,s)\n', '(0,0,b)\n', '(0,0,o)\n', '(0,0,r)\n', '(0,0,n)\n', '(0,0,i)\n', '(1,2,s)\n', '(1,1,m)\n', '(0,0,a)\n', '(1,1,t)\n', '(0,0,o)\n', '(0,0,t)\n', '--s--', '(0,0,c)\n', '(0,0,u)\n', '(0,0,n)\n', '(0,0,d)\n', '(0,0,i)\n', '(3,1,a)\n', '(0,0,m)\n', '(1,1,s)\n', '(0,0,c)\n', '(0,0,a)\n', '(1,4,d)\n', '(2,3,u)\n', '(0,0,c)\n', '(0,0,u)\n', '(0,0,r)\n', '(0,1,e)\n', '(0,0,n)\n', '(0,0,t)\n', '(0,0,l)\n', '(0,0,y)\n', '--s--', '(0,0,h)\n', '(0,0,a)\n', '(0,0,s)\n', '(0,0,t)\n', '(0,0,w)\n', '(0,0,e)\n', '(0,0,n)\n', '(3,2,m)\n', '--s--', '(3,1,w)\n', '(0,0,o)\n', '(2,1,g)\n', '(0,0,e)\n', '(0,0,a)\n', '(0,0,r)\n', '(0,0,s)\n', '--s--', '(0,0,o)\n', '(0,0,l)\n', '(0,0,d)\n', '(0,0,.)\n', '(0,0,f)\n', '(0,0,o)\n', '(0,0,r)\n', '(0,0,m)\n', '(0,0,y)\n', '(0,0,t)\n', '(0,0,h)\n', '(0,0,e)\n', '(0,0,s)\n', '(0,0,i)\n', '(0,0,s)\n', '(0,0,i)\n', '(0,0,w)\n', '(0,0,o)\n', '(0,0,r)\n', '(0,0,k)\n', '(0,0,e)\n', '(0,0,d)\n', '--s--', '(0,0,o)\n', '(0,0,n)\n', '(0,0,i)\n', '(1,1,t)\n', '(0,0,o)\n', '(0,0,r)\n', '(0,0,m)\n', '(0,0,a)\n', '(0,0,t)\n', '(0,0,i)\n', '(0,0,o)\n', '(0,0,n)\n', '--s--', '(2,1,h)\n', '(0,0,e)\n', '(0,0,o)\n', '(0,0,r)\n', '(0,0,y)\n', '--s--', '(0,0,a)\n', '(0,0,n)\n', '(0,0,d)\n', '(0,0,s)\n', '(0,0,t)\n', '(0,0,i)\n', '(0,0,l)\n', '(0,0,l)\n', '(0,0,w)\n', '(0,0,o)\n', '(0,0,r)\n', '(0,0,k)\n', '(0,0,i)\n', '(0,0,n)\n', '(0,0,g)\n', '--s--', '(0,0,o)\n', '(0,0,n)\n', '(0,0,i)\n', '(0,0,t)\n', '(0,0,u)\n', '(0,0,n)\n', '(2,1,e)\n', '(0,0,l)\n', '--s--', '(0,0,\ufeff)\n', '(0,0,w)\n', '(0,0,.)\n', '(0,1,M)\n', '(1,1,w)\n', '(0,0,i)\n', '(0,0,c)\n', '(0,0,a)\n', '(0,0,n)\n', '(0,0,m)\n', '(3,2,b)\n', '(0,0,e)\n', '(0,0,s)\n', '(0,0,o)\n', '(0,0,m)\n', '(0,1,t)\n', '(0,0,h)\n', '(0,0,i)\n', '(0,0,n)\n', '(0,0,g)\n', '--s--', '(0,0,\ufeff)\n', '(0,0,e)\n', '(0,0,a)\n', '(0,0,t)\n', '--s--', '(0,0,s)\n', '(0,0,o)\n', '(4,1,n)\n', '(0,0,.)\n', '--s--', '(0,0,t)\n', '(0,0,h)\n', '(0,0,i)\n', '(0,0,s)\n', '(0,0,i)\n', '(1,1, )\n', '(0,0,y)\n', '(1,1,o)\n', '(0,0,r)\n', '(0,0,e)\n', '(0,0,a)\n', '(0,0,m)\n', '(0,0,.)\n', '--s--', '(0,0,t)\n', '(0,0,h)\n', '(0,0,a)\n', '(0,0,n)\n', '(0,0,k)\n', '(0,0,s)\n', '--s--', '(0,0,f)\n', '(0,0,o)\n', '(0,0,r)\n', '(0,0,y)\n', '(0,1,u)\n', '(4,1,k)\n', '(0,0,i)\n', '(0,0,m)\n', '(0,0,e)\n', '(0,0,a)\n', '(0,0,n)\n', '(3,2,t)\n', '(0,0,h)\n', '(1,2,r)\n', '(0,0,e)\n', '(0,0,a)\n', '(0,0,g)\n', '(0,0,r)\n', '(0,0,e)\n', '(0,1,t)\n', '--s--', '(0,0,d)\n', '(4,1,l)\n', '(0,0,.)\n', '(1,1,E)\n', '(0,0,v)\n', '(0,0,e)\n', '(0,0,y)\n', '(0,0,o)\n', '(0,0,u)\n', '(0,0,s)\n', '(0,0,\\)\n', '(0,0,n)\n', '(0,2,r)\n', '(0,0,u)\n', '(0,0,d)\n', '(4,1,l)\n', '(0,0,.)\n']

    return 0


main()
