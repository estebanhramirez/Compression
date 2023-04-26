"""
    Title:
    Author:
    Date:
"""


import numpy as np
import matplotlib.pyplot as plt
from count_n_grams import count_n_grams
from n_gram_probability import n_gram_probability
from make_probability_matrix import make_probability_matrix

from shannon_entropy import shannon_entropy as uncertainty


def average_uncertainty(n_gram_counts, probability_matrix):
    average = 0
    for previous_n_gram in probability_matrix.index:
        probability = n_gram_probability(previous_n_gram, n_gram_counts)
        average += probability*uncertainty(previous_n_gram, probability_matrix)
    return (average)


def relative_information(previous_n_gram, previous_n_minus1_gram, probability_matrix, probability_matrix_minus1):
    divergence = 0
    for nxt in probability_matrix.columns:
        conditional_prob = probability_matrix.loc[[previous_n_gram]][nxt][0]
        conditional_prob_minus1 = probability_matrix_minus1.loc[[previous_n_minus1_gram]][nxt][0]
        divergence += conditional_prob*np.log(conditional_prob/conditional_prob_minus1)
    return (divergence)


def correlation_information(n_gram_counts, probability_matrix, probability_matrix_minus1):
    correlation = 0
    for previous_n_gram in probability_matrix.index:
        probability = n_gram_probability(previous_n_gram, n_gram_counts)
        previous_n_minus1_gram = previous_n_gram[1:]
        correlation += probability*relative_information(previous_n_gram, previous_n_minus1_gram, probability_matrix, probability_matrix_minus1)
    return (correlation)


def plot(sentences, unique_words, k):
    averages = []
    correlations = []
    effective_measure_complexity = 0
    for i in range(1, 10):
        print(i,'...')
        previous_n_gram_length = i

        n_gram_counts = count_n_grams(sentences, previous_n_gram_length)
        n_plus1_gram_counts = count_n_grams(sentences, previous_n_gram_length+1)

        probability_matrix = make_probability_matrix(n_plus1_gram_counts, unique_words, k)
        probability_matrix_minus1 = make_probability_matrix(n_gram_counts, unique_words, k)

        average = average_uncertainty(n_gram_counts, probability_matrix)
        correlation = correlation_information(n_gram_counts, probability_matrix, probability_matrix_minus1)
        effective_measure_complexity += (i-1)*correlation

        averages.append(average)
        correlations.append(correlation)

    plt.plot(averages)
    plt.savefig('averages_pat2')
    plt.close()
    plt.plot(correlations)
    plt.title('y(x) := mejora entre x y (x+1)')
    plt.savefig('correlations_pat2')
    plt.close()

    print(effective_measure_complexity)


def local_info_patterns(sentences, unique_words, sentence, n):
    patterns = []

    k = 0.01
    previous_n_gram_length = n

    n_plus1_gram_counts = count_n_grams(sentences, previous_n_gram_length+1)
    probability_matrix = make_probability_matrix(n_plus1_gram_counts, unique_words, k)

    sentence = ['<s>']*n + sentence + ['<e>']
    print("sentences:", sentence)
    for i in range(n+1, len(sentence)):
        conf = sentence[i-1]
        locality = sentence[i-n-1:i-1]
        print(tuple(locality), conf)
        if tuple(locality) in probability_matrix.index:
            prob = probability_matrix.loc[[tuple(locality)]][conf][0]
        else:
            prob = k
        local_information = np.log(1/prob)
        patterns.append(local_information)
    print(patterns)
    plt.plot(patterns)
    plt.grid()
    plt.xlabel("string position")
    plt.savefig('patterns')
    plt.close()


def experiment(sentences, unique_words, sentence):
    patterns = []

    k = 0.01
    previous_n_gram_length = 1
    n = previous_n_gram_length

    sentence = ['<s>']*n + sentence + ['<e>']
    suffix = ()
    while n < 10:
        n_plus1_gram_counts = count_n_grams(sentences, n+1)
        probability_matrix = make_probability_matrix(n_plus1_gram_counts, unique_words, k)

        max_idx = 0
        maxi = probability_matrix.loc[[probability_matrix.index[max_idx]]][('a')][0]

        for i, idx in enumerate(probability_matrix.index):
            cur_max = probability_matrix.loc[[tuple(idx)]][('a')][0]
            print(idx[-len(suffix):], "vs", suffix)
            if cur_max >= maxi and idx[-len(suffix):] == suffix:
                maxi = cur_max
                max_idx = i

        suffix = probability_matrix.index[max_idx]
        print(probability_matrix.index[max_idx], ('a'))
        patterns.append(probability_matrix.loc[[probability_matrix.index[max_idx]]][('a')][0])
        n += 1

    print(patterns)
    plt.plot(patterns)
    plt.grid()
    plt.xlabel("string position")
    plt.savefig('patterns inverse')
    plt.close()


def main():
    k = 0.01
    previous_n_gram_length = 1

    unique_words = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',' j', 'k', 'l', 'm', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] # list(set(sum(sentences, [])))

    # TRAINNING SET
    txt1 = ['a', 'a', 'b']*1000
    txt2 = ['a', 'a', 'a']*1000
    txt3 = ['a', 'b', 'b']*1000
    txt4 = ['b', 'b', 'a']*1000
    txt5 = ['b', 'b', 'a']*1000
    txt6 = ['b', 'a', 'b']*1000
    txt7 = ['b', 'a', 'a']*1000
    txt8 = ['b', 'b', 'b']*1000
    txt9 = ['a', 'a', 'a']*1000
    sentences = [txt1, txt2, txt3, txt4, txt5, txt6, txt7, txt8, txt9]

    # PROBABILITY MODELS
    n_minus1_gram_counts = count_n_grams(sentences, previous_n_gram_length-1)
    n_gram_counts = count_n_grams(sentences, previous_n_gram_length)
    n_plus1_gram_counts = count_n_grams(sentences, previous_n_gram_length+1)

    probability_matrix_minus1 = make_probability_matrix(n_gram_counts, unique_words, k)
    probability_matrix = make_probability_matrix(n_plus1_gram_counts, unique_words, k)

    print(probability_matrix_minus1)
    print(probability_matrix)

    average_minus1 = average_uncertainty(n_minus1_gram_counts, probability_matrix_minus1)
    print(average_minus1)

    average = average_uncertainty(n_gram_counts, probability_matrix)
    print(average)

    correlation = correlation_information(n_gram_counts, probability_matrix, probability_matrix_minus1)
    print(correlation)

    #local_info_patterns(sentences, unique_words, txt, previous_n_gram_length)

    #experiment(sentences, unique_words, txt)

    #plot(sentences, unique_words, k)


main()
