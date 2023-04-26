from count_n_grams import count_n_grams
from estimate_probability import estimate_probability


def estimate_probabilities(previous_n_gram, n_gram_counts, n_plus1_gram_counts, vocabulary, end_token='<e>', unknown_token="<unk>",  k=1.0):
    """
    Estimate the probabilities of next words using the n-gram counts with k-smoothing

    Args:
        previous_n_gram: A sequence of words of length n
        n_gram_counts: Dictionary of counts of n-grams
        n_plus1_gram_counts: Dictionary of counts of (n+1)-grams
        vocabulary: List of words
        k: positive constant, smoothing parameter
    
    Returns:
        A dictionary mapping from next words to the probability.
    """
    # convert list to tuple to use it as a dictionary key
    previous_n_gram = tuple(previous_n_gram)    

    # add <e> <unk> to the vocabulary
    # <s> is not needed since it should not appear as the next word
    vocabulary = vocabulary + [end_token, unknown_token]    
    vocabulary_size = len(vocabulary)    

    probabilities = {}
    for word in vocabulary:
        probability = estimate_probability(word, previous_n_gram, 
                                           n_gram_counts, n_plus1_gram_counts, 
                                           vocabulary_size, k=k)
        probabilities[word] = probability

    return probabilities


def run():
    previous_n_gram = ['a', 'a', 'b', 'a']

    sentences = [['a', 'a', 'b', 'a', 'b', 'b', 'b', 'b', 'a', 'a', 'b', 'a', 'b'],]
                 #['b', 'b', 'a', 'b', 'a', 'a', 'a', 'a', 'b', 'b', 'a', 'b', 'a']]

    unique_words = list(set(sentences[0]))
    n_gram_counts = count_n_grams(sentences, len(previous_n_gram))
    n_plus1_gram_counts = count_n_grams(sentences, len(previous_n_gram)+1)

    probabilities = estimate_probabilities(previous_n_gram, n_gram_counts, n_plus1_gram_counts, unique_words, k=0)
    print(probabilities)

run()