import numpy as np
from count_n_grams import count_n_grams
from make_probability_matrix import make_probability_matrix


def debug(n_gram_counts, probability_matrix):
    print(probability_matrix)
    print(n_gram_counts)
    probability = n_gram_probability(('b', '<e>'), n_gram_counts)
    print(probability)
    cnt = 0
    for index in probability_matrix.index:
        probability = n_gram_probability(index, n_gram_counts)
        cnt += probability
    print(cnt)


def n_gram_probability(n_gram, n_gram_counts):
    probability = n_gram_counts[n_gram] / sum(n_gram_counts.values())
    return (probability)


def uncertainty(previous_n_gram, probability_matrix):
    entropy = 0
    for nxt in probability_matrix.columns:
        conditional_prob = probability_matrix.loc[[previous_n_gram]][nxt][0]
        entropy += conditional_prob*np.log(1/conditional_prob)
    return (entropy)


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
        #if nxt in probability_matrix_minus1.columns:
        #    conditional_prob_minus1 = probability_matrix_minus1.loc[[previous_n_minus1_gram]][nxt][0]
        #else:
        #    conditional_prob_minus1 = 0
        divergence += conditional_prob*np.log(conditional_prob/conditional_prob_minus1)
    return (divergence)


def correlation_information(n_gram_counts, probability_matrix, probability_matrix_minus1):
    correlation = 0
    for previous_n_gram in probability_matrix.index:
        probability = n_gram_probability(previous_n_gram, n_gram_counts)
        previous_n_minus1_gram = previous_n_gram[1:]
        correlation += probability*relative_information(previous_n_gram, previous_n_minus1_gram, probability_matrix, probability_matrix_minus1)
    return (correlation)


def main():
    k = 1
    previous_n_gram_length = 4
    sentences = [['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a']]
    unique_words = list(set(sum(sentences, [])))

    n_gram_counts = count_n_grams(sentences, previous_n_gram_length)
    #n_minus1_gram_counts = count_n_grams(sentences, previous_n_gram_length-1)

    n_plus1_gram_counts = count_n_grams(sentences, previous_n_gram_length+1)
    probability_matrix = make_probability_matrix(n_plus1_gram_counts, unique_words, k)
    probability_matrix_minus1 = make_probability_matrix(n_gram_counts, unique_words, k)

    average = average_uncertainty(n_gram_counts, probability_matrix)
    print(average)

    correlation = correlation_information(n_gram_counts, probability_matrix, probability_matrix_minus1)
    print(correlation)


main()
