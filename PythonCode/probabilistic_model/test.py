"""
    Title:
    Author:
    Date:
"""


import numpy as np
from count_n_grams import count_n_grams
from n_gram_probability import n_gram_probability
from make_probability_matrix import make_probability_matrix

from shannon_entropy import shannon_entropy as uncertainty


def average_uncertainty(n_gram_counts, probability_matrix):
    average = 0
    for previous_n_gram in probability_matrix.index:
        probability = n_gram_probability(previous_n_gram, n_gram_counts)
        average += probability*uncertainty(previous_n_gram, probability_matrix)

    return average


def relative_information(previous_n_gram, previous_n_minus1_gram, probability_matrix, probability_matrix_minus1, k):
    divergence = 0
    for nxt in probability_matrix.columns:
        try:
            conditional_prob = probability_matrix.loc[[previous_n_gram]][nxt][0]
        except KeyError:
            conditional_prob = k

        try:
            conditional_prob_minus1 = probability_matrix_minus1.loc[[previous_n_minus1_gram]][nxt][0]
        except KeyError:
            conditional_prob_minus1 = k

        divergence += conditional_prob*np.log(conditional_prob/conditional_prob_minus1)

    return divergence


def correlation_information(n_gram_counts, probability_matrix, probability_matrix_minus1, k):
    correlation = 0
    for previous_n_gram in probability_matrix.index:
        probability = n_gram_probability(previous_n_gram, n_gram_counts)
        previous_n_minus1_gram = previous_n_gram[1:]
        correlation += probability*relative_information(previous_n_gram, previous_n_minus1_gram, probability_matrix, probability_matrix_minus1, k)

    return correlation


def find_patterns(sentences, unique_words, k, previous_n_gram, prev_prob):
    print("P(",previous_n_gram,") = ", prev_prob)

    previous_n_gram_length = len(previous_n_gram)
    n_plus1_gram_counts = count_n_grams(sentences, previous_n_gram_length+1)

    probability_matrix = make_probability_matrix(n_plus1_gram_counts, unique_words, k)

    try:
        entropy = uncertainty(previous_n_gram, probability_matrix)
    except KeyError:
        entropy = 0

    threshold = entropy
    for nxt in probability_matrix.columns:
        if tuple(previous_n_gram) in probability_matrix.index:
            prob = probability_matrix.loc[[tuple(previous_n_gram)]][nxt][0]
        else:
            prob = k

        if np.log(1/prob)/prob < threshold:
            find_patterns(sentences, unique_words, k, previous_n_gram+[nxt], prev_prob*prob)


def find_patterns_wrapper(sentences, unique_words, k, previous_n_gram):
    previous_n_gram_length = len(previous_n_gram)
    n_plus1_gram_counts = count_n_grams(sentences, previous_n_gram_length+1)
    probability_matrix = make_probability_matrix(n_plus1_gram_counts, unique_words, k)
    for nxt in probability_matrix.columns:
        find_patterns(sentences, unique_words, k, previous_n_gram+[nxt], probability_matrix.loc[[tuple(previous_n_gram)]][nxt][0])
        print('\n\n')


def main():
    k = 0.01
    unique_words = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] # list(set(sum(sentences, [])))

    txt = ['e', 's', 't', 'e', 'b', 'a', 'n', 'h', 'e', 'r', 'n', 'a', 'n', 'd', 'e', 'z', 'r', 'a', 'm', 'i', 'r', 'e', 'z']
    sentences = [txt]

    find_patterns_wrapper(sentences, unique_words, k, [])


main()
