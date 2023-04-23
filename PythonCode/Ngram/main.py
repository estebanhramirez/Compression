import os
import numpy as np
import matplotlib.pyplot as plt
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

        #print(average, correlation)
        averages.append(average)
        correlations.append(correlation)
    averages = averages
    correlations = correlations

    plt.plot(averages)
    plt.savefig('averages_pat2')
    plt.close()
    plt.plot(correlations)
    plt.title('y(x) := mejora entre x y (x+1)')
    plt.savefig('correlations_pat2')
    plt.close()
    print("--------------------------------------->", effective_measure_complexity)


def local_info_patterns(sentences, unique_words, sentence, n):
    patterns = []

    k = 0.01
    previous_n_gram_length = n

    n_plus1_gram_counts = count_n_grams(sentences, previous_n_gram_length+1)
    probability_matrix = make_probability_matrix(n_plus1_gram_counts, unique_words, k)

    sentence = ['<s>']*n + sentence + ['<e>']
    print(sentence)
    for i in range(n+1, len(sentence)):
        conf = sentence[i]
        locality = sentence[i-n-1:i-1]
        print(tuple(locality))
        prob = probability_matrix.loc[[tuple(locality)]][conf][0]
        local_information = np.log(1/prob)
        patterns.append(local_information)
    plt.plot(patterns)
    plt.savefig('patterns')
    plt.close()


def main():
    """
    path = 'data/TXTs/dummy.txt'
    dir_path = os.path.dirname(os.path.realpath(path))
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            with open(dir_path+'/'+file, 'r') as f:
                txt = f.read()
                #txt = txt[10000:15000]
    """
    k = 0.01
    previous_n_gram_length = 2

    txt1 = ['a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b']
    txt2 = ['a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b']
    txt3 = ['a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b']
    txt4 = ['a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b']
    txt5 = ['a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'c', 'b', 'a', 'b', 'a', 'c', 'a', 'b', 'a', 'b', 'a', 'b']
    sentences = [txt1, txt2, txt3, txt4, txt5] #[txt[0:100], txt[100:200], txt[200:300], txt[300:400], txt[400:500]] # [['a', 'b', 'a', 'c', 'a', 'd', 'a', 'f', 'a', 'g', 'a', 'h', 'a', 'i', 'a', 'j', 'a', 'k', 'a', 'l', 'a', 'm', 'a', 'n', 'a', 'o'], ['a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e'], ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',' u', 'v', 'w', 'x', 'y', 'z'], ['e', 's', 't', 'e', 'b', 'a', 'n', 'h', 'e', 'r', 'n', 'a', 'n', 'd', 'e', 'z', 'e', 's', 't', 'e', 'b', 'a', 'n', 'h', 'e', 'r', 'n', 'a', 'n', 'd', 'e', 'z'], ['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c']]
    unique_words = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',' j', 'k', 'l', 'm', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] # list(set(sum(sentences, [])))
    #plot(sentences)


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

    local_info_patterns(sentences, unique_words, txt5, 2)


main()
