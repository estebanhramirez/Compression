from count_n_grams import count_n_grams
from make_probability_matrix import make_probability_matrix

def extend(search_buffer, unique_words, probability_matrix):
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
    return maxword

def run():
    previous_n_gram_length = 3

    sentences = [['a', 'a', 'b', 'a', 'b', 'b', 'b', 'b', 'a', 'a', 'b', 'a', 'b'],]
                 #['b', 'b', 'a', 'b', 'a', 'a', 'a', 'a', 'b', 'b', 'a', 'b', 'a']]

    unique_words = list(set(sentences[0]))
    n_plus1_gram_counts = count_n_grams(sentences, previous_n_gram_length+1)

    probability_matrix = make_probability_matrix(n_plus1_gram_counts, unique_words, k=0)
    print(probability_matrix)
    #print(count_matrix.iloc[9])
    #print(probability_matrix.loc[[('b', 'a', 'a')]])
    #print(probability_matrix.loc[[('<s>', '<s>', '<s>')]])
    #print()
    #print(probability_matrix.loc[[('<s>', '<s>', '<s>')]]['<unk>'])

    for i in range(0, 3):
        nextword = extend('baa', unique_words, probability_matrix)
            


run()