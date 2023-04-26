from count_n_grams import count_n_grams
from make_count_matrix import make_count_matrix

def make_probability_matrix(n_plus1_gram_counts, vocabulary, k=1.0):
    count_matrix = make_count_matrix(n_plus1_gram_counts, vocabulary)
    count_matrix += k
    prob_matrix = count_matrix.div(count_matrix.sum(axis=1), axis=0)
    return prob_matrix


def run():
    previous_n_gram_length = 3

    sentences = [['a', 'a', 'b', 'a', 'b', 'b', 'b', 'b', 'a', 'a', 'b', 'a', 'b'],]
                 #['b', 'b', 'a', 'b', 'a', 'a', 'a', 'a', 'b', 'b', 'a', 'b', 'a']]

    unique_words = list(set(sentences[0]))
    n_plus1_gram_counts = count_n_grams(sentences, previous_n_gram_length+1)

    print('bigram counts')
    probability_matrix = make_probability_matrix(n_plus1_gram_counts, unique_words, k=0)
    print(probability_matrix)
    #print(count_matrix.iloc[9])
    print(probability_matrix.loc[[('b', 'a', 'a')]])
    print(probability_matrix.loc[[('<s>', '<s>', '<s>')]])
    print()
    print(probability_matrix.loc[[('<s>', '<s>', '<s>')]]['a'])

#run()