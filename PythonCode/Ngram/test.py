import numpy as np
from count_n_grams import count_n_grams
from make_probability_matrix import make_probability_matrix


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


def find_patterns_wrapper(sentences, unique_words, k, previous_n_gram):
    print(previous_n_gram)
    threshold = 0.7

    previous_n_gram_length = len(previous_n_gram)

    n_gram_counts = count_n_grams(sentences, previous_n_gram_length)
    n_plus1_gram_counts = count_n_grams(sentences, previous_n_gram_length+1)
    probability_matrix = make_probability_matrix(n_plus1_gram_counts, unique_words, k)

    entropy = uncertainty(previous_n_gram, probability_matrix)
    print("entropy:", entropy)
    #average = average_uncertainty(n_gram_counts, probability_matrix)
    #print("average uncertainty:", average)
    for nxt in probability_matrix.columns:
        if tuple(previous_n_gram) in probability_matrix.index:
            prob = probability_matrix.loc[[tuple(previous_n_gram)]][nxt][0]
        else:
            prob = 0

        print(prob)
        if prob > threshold:
            find_patterns_wrapper(sentences, unique_words, k, previous_n_gram+[nxt])


def find_patterns(sentences, unique_words, k, previous_n_gram):
    previous_n_gram_length = len(previous_n_gram)
    n_plus1_gram_counts = count_n_grams(sentences, previous_n_gram_length+1)
    probability_matrix = make_probability_matrix(n_plus1_gram_counts, unique_words, k)
    for nxt in probability_matrix.columns:
        find_patterns_wrapper(sentences, unique_words, k, previous_n_gram+[nxt])
        print('----------------------------------------------------------------------')


def main():
    k = 0.01
    previous_n_gram_length = 1

    unique_words = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] # list(set(sum(sentences, [])))

    # TRAINNING SET
    txt = ['a', 'b', 'a', 'b', 'a', 'b', 'c', 'c', 'c', 'c', 'd', 'e', 'd', 'e', 'd', 'e', 'f'] # threshold = 0.70
    #txt =  ['a', 'b', 'c', 'd']*20  # threshold = 0.95
    sentences = [txt]


    find_patterns(sentences, unique_words, k, [])


main()
