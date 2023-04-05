import numpy as np
import os
from count_n_grams import count_n_grams
from itertools import product
from make_probability_matrix import make_probability_matrix


def find(search_buffer, unique_words, probability_matrix):
    unique_words = unique_words + ["<e>", "<unk>"]
    search_buffer = tuple(list(search_buffer))
    
    entropy = 0

    maxword = ''
    maxprob = 0
    for word in unique_words:
        prob = probability_matrix.loc[[search_buffer]][word]
        prob = prob[0]
        entropy += prob*np.log(prob)
        if prob > maxprob:
            maxprob = prob
            maxword = word
    entropy = -entropy
    print(entropy)
    return maxword, maxprob


def naive_extend(search_buffer_ini, sentences, unique_words, k):
    search_buffer = search_buffer_ini
    nextword = '' 
    extension = ''
    while nextword != '<e>' and extension in search_buffer_ini+extension[:-1]:
        previous_n_gram_length = len(search_buffer)

        n_plus1_gram_counts = count_n_grams(sentences, previous_n_gram_length+1)

        probability_matrix = make_probability_matrix(n_plus1_gram_counts, unique_words, k)

        nextword, _ = find(search_buffer, unique_words, probability_matrix)
        search_buffer += nextword
        extension += nextword
    print(search_buffer_ini+'|'+extension[:])


def entropy_naive_extend(sentences, unique_words, k):
    previous_n_gram_length = 100
    n_plus1_gram_counts = count_n_grams(sentences, previous_n_gram_length+1)
    probability_matrix = make_probability_matrix(n_plus1_gram_counts, unique_words, k=0)
    for i in probability_matrix.index:
        if not '<s>' in list(i) and not '<e>' in list(i):
            naive_extend(''.join(i), sentences, unique_words, k)
    print("DONE")


def k_permutations(unique_words, k):
    return ([''.join(x) for x in product(unique_words, repeat=k)])


def run():
    path = 'data/TXTs/dummy.txt'
    dir_path = os.path.dirname(os.path.realpath(path))
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            with open(dir_path+'/'+file, 'r') as f:
                txt = f.read()
                txt = txt[0:1000]
                sentences = [list(txt)] # [['a', 'b', 'a', 'a', 'b', 'a', 'a', 'b', 'a', 'a', 'b', 'a', 'a', 'b', 'a', 'a', 'b', 'a']] #[['a', 'a', 'b', 'a', 'b', 'b', 'b', 'b', 'a', 'a', 'b', 'a', 'b'], ['b', 'b', 'a', 'b', 'a', 'a', 'a', 'a', 'b', 'b', 'a', 'b', 'a']]
                print(sentences)
                unique_words = list(set(sentences[0]))
                #search_buffer_ini = 'baa'
                #naive_extend(search_buffer_ini, sentences, unique_words)
                entropy_naive_extend(sentences, unique_words, k=1)

run()
# HERE WE ARE :)