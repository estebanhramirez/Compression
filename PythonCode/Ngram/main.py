import os
import numpy as np
import matplotlib.pyplot as plt
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
        divergence += conditional_prob*np.log(conditional_prob/conditional_prob_minus1)
    return (divergence)


def correlation_information(n_gram_counts, probability_matrix, probability_matrix_minus1):
    correlation = 0
    for previous_n_gram in probability_matrix.index:
        probability = n_gram_probability(previous_n_gram, n_gram_counts)
        previous_n_minus1_gram = previous_n_gram[1:]
        correlation += probability*relative_information(previous_n_gram, previous_n_minus1_gram, probability_matrix, probability_matrix_minus1)
    return (correlation)


def plot(sentences):
    k = 1
    unique_words = list(set(sum(sentences, [])))
    averages = []
    correlations = []
    for i in range(1, 100):
        print(i,'...')
        previous_n_gram_length = i

        n_gram_counts = count_n_grams(sentences, previous_n_gram_length)
        n_plus1_gram_counts = count_n_grams(sentences, previous_n_gram_length+1)

        probability_matrix = make_probability_matrix(n_plus1_gram_counts, unique_words, k)
        probability_matrix_minus1 = make_probability_matrix(n_gram_counts, unique_words, k)

        average = average_uncertainty(n_gram_counts, probability_matrix)
        correlation = correlation_information(n_gram_counts, probability_matrix, probability_matrix_minus1)
        #print(average, correlation)
        averages.append(average)
        correlations.append(correlation)
    averages = [averages[0]] + averages
    correlations = [correlations[0]] + correlations

    plt.plot(averages)
    plt.savefig('averages')
    plt.close()
    plt.plot(correlations)
    plt.savefig('correlations')
    plt.close()


def main():
    #k = 1
    #previous_n_gram_length = 2
    path = 'data/TXTs/dummy.txt'
    dir_path = os.path.dirname(os.path.realpath(path))
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            with open(dir_path+'/'+file, 'r') as f:
                txt = f.read()
                #txt = txt[10000:15000]
                txt = list(txt)
                sentences = [txt[0:100], txt[100:200], txt[200:300], txt[300:400], txt[400:500]] # [['a', 'b', 'a', 'c', 'a', 'd', 'a', 'f', 'a', 'g', 'a', 'h', 'a', 'i', 'a', 'j', 'a', 'k', 'a', 'l', 'a', 'm', 'a', 'n', 'a', 'o'], ['a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e'], ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',' u', 'v', 'w', 'x', 'y', 'z'], ['e', 's', 't', 'e', 'b', 'a', 'n', 'h', 'e', 'r', 'n', 'a', 'n', 'd', 'e', 'z', 'e', 's', 't', 'e', 'b', 'a', 'n', 'h', 'e', 'r', 'n', 'a', 'n', 'd', 'e', 'z'], ['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c']]
                plot(sentences)

    #unique_words = list(set(sum(sentences, [])))
    """
    n_gram_counts = count_n_grams(sentences, previous_n_gram_length)
    #n_minus1_gram_counts = count_n_grams(sentences, previous_n_gram_length-1)

    n_plus1_gram_counts = count_n_grams(sentences, previous_n_gram_length+1)
    probability_matrix = make_probability_matrix(n_plus1_gram_counts, unique_words, k)
    probability_matrix_minus1 = make_probability_matrix(n_gram_counts, unique_words, k)

    average = average_uncertainty(n_gram_counts, probability_matrix)
    print(average)

    correlation = correlation_information(n_gram_counts, probability_matrix, probability_matrix_minus1)
    print(correlation)
    """
    


main()
