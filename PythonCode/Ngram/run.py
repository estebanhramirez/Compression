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
    sentences = [['a', 'a', 'b', 'a', 'b', 'b', 'b', 'b', 'a', 'a', 'b', 'a', 'b'],]
                 #['b', 'b', 'a', 'b', 'a', 'a', 'a', 'a', 'b', 'b', 'a', 'b', 'a']]
    unique_words = list(set(sentences[0]))

    search_buffer_ini = 'baa'
    search_buffer = search_buffer_ini
    nextword = '' 
    extension = ''
    while nextword != '<e>' and extension in search_buffer_ini:
        print(search_buffer)
        previous_n_gram_length = len(search_buffer)

        n_plus1_gram_counts = count_n_grams(sentences, previous_n_gram_length+1)

        probability_matrix = make_probability_matrix(n_plus1_gram_counts, unique_words, k=0)

        nextword = extend(search_buffer, unique_words, probability_matrix)
        search_buffer += nextword
        extension += nextword
    print(search_buffer, '<-----')


run()