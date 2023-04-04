from count_n_grams import count_n_grams
from itertools import product
from make_probability_matrix import make_probability_matrix

def find(search_buffer, unique_words, probability_matrix):
    unique_words = unique_words + ["<e>", "<unk>"]
    search_buffer = tuple(list(search_buffer))
    
    maxword = ''
    maxprob = 0
    for word in unique_words:
        prob = probability_matrix.loc[[search_buffer]][word]
        prob = prob[0]
        if prob > maxprob:
            maxprob = prob
            maxword = word
    return maxword, maxprob


def extend(search_buffer, unique_words, probability_matrix):
    print()


def naive_extend(search_buffer_ini, sentences, unique_words):
    search_buffer = search_buffer_ini
    nextword = '' 
    extension = ''
    while nextword != '<e>' and extension in search_buffer_ini:
        previous_n_gram_length = len(search_buffer)

        n_plus1_gram_counts = count_n_grams(sentences, previous_n_gram_length+1)

        probability_matrix = make_probability_matrix(n_plus1_gram_counts, unique_words, k=0)

        nextword, _ = find(search_buffer, unique_words, probability_matrix)
        search_buffer += nextword
        extension += nextword
    print(search_buffer_ini+'|'+extension[:-1])


def entropy_naive_extend(sentences, unique_words):
    previous_n_gram_length = 3
    n_plus1_gram_counts = count_n_grams(sentences, previous_n_gram_length+1)
    probability_matrix = make_probability_matrix(n_plus1_gram_counts, unique_words, k=0)
    for i in probability_matrix.index:
        if not '<s>' in list(i) and not '<e>' in list(i):
            naive_extend(''.join(i), sentences, unique_words)


def k_permutations(unique_words, k):
    return ([''.join(x) for x in product(unique_words, repeat=k)])

def run():
    sentences = [['a', 'a', 'b', 'a', 'b', 'b', 'b', 'b', 'a', 'a', 'b', 'a', 'b'],
                 ['b', 'b', 'a', 'b', 'a', 'a', 'a', 'a', 'b', 'b', 'a', 'b', 'a']]
    unique_words = list(set(sentences[0]+sentences[1]))
    search_buffer_ini = 'baa'

    naive_extend(search_buffer_ini, sentences, unique_words)
    entropy_naive_extend(sentences, unique_words)

run()