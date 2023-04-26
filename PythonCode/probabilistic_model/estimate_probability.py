from count_n_grams import count_n_grams

def estimate_probability(word, previous_n_gram, n_gram_counts, n_plus1_gram_counts, vocabulary_size, k=1.0):
    """
    Estimate the probabilities of a next word using the n-gram counts with k-smoothing
    
    Args:
        word: next word
        previous_n_gram: A sequence of words of length n
        n_gram_counts: Dictionary of counts of n-grams
        n_plus1_gram_counts: Dictionary of counts of (n+1)-grams
        vocabulary_size: number of words in the vocabulary
        k: positive constant, smoothing parameter
    
    Returns:
        A probability
    """
    # convert list to tuple to use it as a dictionary key
    previous_n_gram = tuple(previous_n_gram)

    # Set the denominator
    # If the previous n-gram exists in the dictionary of n-gram counts,
    # Get its count.  Otherwise set the count to zero
    # Use the dictionary that has counts for n-grams
    previous_n_gram_count = n_gram_counts.get(previous_n_gram, 0)
            
    # Calculate the denominator using the count of the previous n gram
    # and apply k-smoothing
    denominator = previous_n_gram_count + k*vocabulary_size

    # Define n plus 1 gram as the previous n-gram plus the current word as a tuple
    n_plus1_gram = tuple(list(previous_n_gram) + [word])
  
    # Set the count to the count in the dictionary,
    # otherwise 0 if not in the dictionary
    # use the dictionary that has counts for the n-gram plus current word    
    n_plus1_gram_count = n_plus1_gram_counts.get(n_plus1_gram, 0)
            
    # Define the numerator use the count of the n-gram plus current word,
    # and apply smoothing
    numerator = n_plus1_gram_count + k
        
    # Calculate the probability as the numerator divided by denominator
    probability = numerator / denominator
    return probability


def run():
    next_symb = 'b'
    previous_n_gram = ['a', 'a', 'b', 'a']

    sentences = [['a', 'a', 'b', 'a', 'b', 'b', 'b', 'b', 'a', 'a', 'b', 'a', 'b']]
    unique_words = list(set(sentences[0]))

    n_gram_counts = count_n_grams(sentences, len(previous_n_gram))
    n_plus1_gram_counts = count_n_grams(sentences, len(previous_n_gram)+1)
    tmp_prob = estimate_probability(next_symb, previous_n_gram, n_gram_counts, n_plus1_gram_counts, len(unique_words), k=0)

    print(f"The estimated probability of word '{next_symb}' given the previous n-gram {previous_n_gram} is: {tmp_prob:.4f}")

run()