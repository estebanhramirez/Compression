import numpy as np
import pandas as pd
from count_n_grams import count_n_grams


def make_count_matrix(n_plus1_gram_counts, vocabulary):
    # add <e> <unk> to the vocabulary
    # <s> is omitted since it should not appear as the next word
    vocabulary = vocabulary + ["<e>", "<unk>"]
    
    # obtain unique n-grams
    n_grams = []
    for n_plus1_gram in n_plus1_gram_counts.keys():
        n_gram = n_plus1_gram[0:-1]        
        n_grams.append(n_gram)
    n_grams = list(set(n_grams))
    
    # mapping from n-gram to row
    row_index = {n_gram:i for i, n_gram in enumerate(n_grams)}    
    # mapping from next word to column
    col_index = {word:j for j, word in enumerate(vocabulary)}    
    
    nrow = len(n_grams)
    ncol = len(vocabulary)
    count_matrix = np.zeros((nrow, ncol))
    for n_plus1_gram, count in n_plus1_gram_counts.items():
        n_gram = n_plus1_gram[0:-1]
        word = n_plus1_gram[-1]
        if word not in vocabulary:
            continue
        i = row_index[n_gram]
        j = col_index[word]
        count_matrix[i, j] = count
    
    count_matrix = pd.DataFrame(count_matrix, index=n_grams, columns=vocabulary)
    return count_matrix

def run():
    previous_n_gram_length = 2

    sentences = [['a', 'a', 'b', 'a', 'b', 'b', 'b', 'b', 'a', 'a', 'b', 'a', 'b'],]
                 #['b', 'b', 'a', 'b', 'a', 'a', 'a', 'a', 'b', 'b', 'a', 'b', 'a']]

    unique_words = list(set(sentences[0]))
    n_plus1_gram_counts = count_n_grams(sentences, previous_n_gram_length+1)

    print('bigram counts')
    print(make_count_matrix(n_plus1_gram_counts, unique_words))


run()