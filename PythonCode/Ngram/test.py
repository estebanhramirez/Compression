from count_n_grams import count_n_grams
from make_probability_matrix import make_probability_matrix


def first_approach(sentences, unique_words, k, previous_n_gram_length):
    n_plus1_gram_counts = count_n_grams(sentences, previous_n_gram_length+1)
    probability_matrix = make_probability_matrix(n_plus1_gram_counts, unique_words, k)
    for idx in probability_matrix.index:
        suffixes = []
        for i in range(0, len(list(idx))):
            suffixes.append(idx[i:])

        for suffix in suffixes:
            in_probability_matrix = probability_matrix.copy()
            previous_n_gram = idx
            cnt = 0
            word = suffix[cnt]
            if previous_n_gram in in_probability_matrix.index and word in in_probability_matrix.columns:
                prob = in_probability_matrix.loc[[previous_n_gram]][word][0]#+in_probability_matrix.loc[[previous_n_gram]]['<e>'][0]
            else:
                prob = 0
            print('P(',word,'|',''.join(previous_n_gram),')=',prob, '----> cnt:', cnt)

            while prob > 0:
                previous_n_gram += tuple(word)
                suffix += tuple(word)
                cnt += 1
                if cnt >= len(suffix):
                    break
                word = suffix[cnt]

                in_n_plus1_gram_counts = count_n_grams(sentences, previous_n_gram_length+cnt+1)
                in_probability_matrix = make_probability_matrix(in_n_plus1_gram_counts, unique_words, k)
                if previous_n_gram in in_probability_matrix.index and word in in_probability_matrix.columns:
                    prob = in_probability_matrix.loc[[previous_n_gram]][word][0]#+in_probability_matrix.loc[[previous_n_gram]]['<e>'][0]
                else:
                    prob = 0
                print('P(',word,'|',''.join(previous_n_gram),')=',prob, '----> cnt:', cnt)
            print()
        print('------------------------------')


def find_patterns_wrapper(sentences, unique_words, k, previous_n_gram):
    print(previous_n_gram)
    threshold = 0.7
    previous_n_gram_length = len(previous_n_gram)
    n_plus1_gram_counts = count_n_grams(sentences, previous_n_gram_length+1)
    probability_matrix = make_probability_matrix(n_plus1_gram_counts, unique_words, k)
    #print(probability_matrix)
    for nxt in probability_matrix.columns:
        if tuple(previous_n_gram) in probability_matrix.index:
            prob = probability_matrix.loc[[tuple(previous_n_gram)]][nxt][0]
        else:
            prob = 0

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
    txt = ['a', 'b', 'a', 'b', 'a', 'b', 'c', 'c', 'c', 'c', 'd', 'e', 'd', 'e', 'd', 'e', 'a'] # threshold = 0.70
    #txt =  ['a', 'b', 'c', 'd']*20  # threshold = 0.95
    sentences = [txt]

    # PROBABILITY MODELS
    #first_approach(sentences, unique_words, k, 2)
    find_patterns(sentences, unique_words, k, [])


main()
