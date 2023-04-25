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


def relative_information(previous_n_gram, previous_n_minus1_gram, probability_matrix, probability_matrix_minus1):
    divergence = 0
    for nxt in probability_matrix.columns:
        try:
            conditional_prob = probability_matrix.loc[[previous_n_gram]][nxt][0]
        except:
            conditional_prob = 0.01
        try:
            conditional_prob_minus1 = probability_matrix_minus1.loc[[previous_n_minus1_gram]][nxt][0]
        except:
            conditional_prob_minus1 = 0.01
        #print(conditional_prob, "vs", conditional_prob_minus1)
        divergence += conditional_prob*np.log(conditional_prob/conditional_prob_minus1)
    return (divergence)


def correlation_information(n_gram_counts, probability_matrix, probability_matrix_minus1):
    correlation = 0
    for previous_n_gram in probability_matrix.index:
        probability = n_gram_probability(previous_n_gram, n_gram_counts)
        previous_n_minus1_gram = previous_n_gram[1:]
        correlation += probability*relative_information(previous_n_gram, previous_n_minus1_gram, probability_matrix, probability_matrix_minus1)
    return (correlation)





def find_patterns_wrapper(sentences, unique_words, k, previous_n_gram):
    print(previous_n_gram)
    threshold = 0.7

    previous_n_gram_length = len(previous_n_gram)

    n_gram_counts = count_n_grams(sentences, previous_n_gram_length)
    n_plus1_gram_counts = count_n_grams(sentences, previous_n_gram_length+1)
    n_plus2_gram_counts = count_n_grams(sentences, previous_n_gram_length+2)

    probability_matrix_minus1 = make_probability_matrix(n_gram_counts, unique_words, k)
    probability_matrix = make_probability_matrix(n_plus1_gram_counts, unique_words, k)
    probability_matrix_plus1 = make_probability_matrix(n_plus2_gram_counts, unique_words, k)

    try:
        entropy = uncertainty(previous_n_gram, probability_matrix)
    except:
        entropy = 0
    #print("entropy:", entropy)

    #average = average_uncertainty(n_gram_counts, probability_matrix)
    #print("average uncertainty:", average)

    #correlation = correlation_information(n_gram_counts, probability_matrix, probability_matrix_minus1)
    #correlation = correlation_information(n_plus1_gram_counts, probability_matrix_plus1, probability_matrix)
    #print("correlation:", correlation)

    threshold = entropy
    print("threshold:", threshold)
    for nxt in probability_matrix.columns:
        if tuple(previous_n_gram) in probability_matrix.index:
            prob = probability_matrix.loc[[tuple(previous_n_gram)]][nxt][0]
        else:
            prob = k

        #print(relative_information(tuple(previous_n_gram+[nxt]), tuple(previous_n_gram[1:]+[nxt]), probability_matrix_plus1, probability_matrix))
        if np.log(1/prob)/prob < threshold:
            print(np.log(1/prob)/prob)
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
    #txt = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] # threshold = 0.70
    #txt = ['a', 'a', 'b', 'b', 'a', 'a', 'b', 'b', 'a', 'a', 'b', 'b', 'c', 'd', 'd', 'e', 'e', 'd', 'd', 'e', 'e']
    #txt = ['a', 'b', 'a', 'b', 'a', 'b', 'c', 'c', 'c', 'c', 'd', 'e', 'd', 'e', 'd', 'e', 'f'] # threshold = 0.70 & threshold = abs(average-entropy)
    #txt =  ['a', 'b', 'c', 'd']*2  # threshold = 0.95
    #txt = ['1', 'b', 'b', '2', '9', '7', 'a', 'a', '3', 'b', 'b', '5', '1', 'a', 'a', '9', '4', 'b', 'b', '8', 'a', 'a', '6', '2', '0', 'b', 'b', 'b', '7', 'b', 'b']
    txt = ['e', 's', 't', 'e', 'b', 'a', 'n', 'h', 'e', 'r', 'n', 'a', 'n', 'd', 'e', 'z', 'r', 'a', 'm', 'i', 'r', 'e', 'z']
    sentences = [txt]


    find_patterns(sentences, unique_words, k, [])


main()
