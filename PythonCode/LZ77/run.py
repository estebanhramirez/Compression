from collections import defaultdict
import numpy as np
import math
import sys
sys.path.insert(0, 'PythonCode/LZ77/compressor')
sys.path.insert(1, 'PythonCode/LZ77/decompressor')

import decompressor.Decompressor as Decompressor
import compressor.Compressor as Compressor

from Decompressor import Decompressor
from Compressor import Compressor


def create_dictionaries(training_corpus, vocab):
    """
    Input: 
        training_corpus: a corpus where each line has a word followed by its tag.
        vocab: a dictionary where keys are words in vocabulary and value is an index
    Output: 
        emission_counts: a dictionary where the keys are (tag, word) and the values are the counts
        transition_counts: a dictionary where the keys are (prev_tag, tag) and the values are the counts
        tag_counts: a dictionary where the keys are the tags and the values are the counts
    """

    # initialize the dictionaries using defaultdict
    emission_counts = defaultdict(int)
    transition_counts = defaultdict(int)
    tag_counts = defaultdict(int)
    # Initialize "prev_tag" (previous tag) with the start state, denoted by '--s--'
    prev_tag = '--s--'
    # use 'i' to track the line number in the corpus
    i = 0
    # Each item in the training corpus contains a word and its POS tag
    # Go through each word and its tag in the training corpus
    for word_tag in training_corpus:
        # Increment the word_tag count
        i += 1
        # get the word and tag using the get_word_tag helper function (imported from utils_pos.py)
        # the function is defined as: get_word_tag(line, vocab)
        word, tag = word_tag
        # Increment the transition count for the previous word and tag
        transition_counts[(prev_tag, tag)] += 1
        # Increment the emission count for the tag and word
        emission_counts[(tag, word)] += 1
        # Increment the tag count
        tag_counts[tag] += 1
        # Set the previous tag to this tag (for the next iteration of the loop)
        prev_tag = tag
    return emission_counts, transition_counts, tag_counts


def predict_pos(prep, y, emission_counts, vocab, states):
    '''
    Input: 
        prep: a preprocessed version of 'y'. A list with the 'word' component of the tuples.
        y: a corpus composed of a list of tuples where each tuple consists of (word, POS)
        emission_counts: a dictionary where the keys are (tag,word) tuples and the value is the count
        vocab: a dictionary where keys are words in vocabulary and value is an index
        states: a sorted list of all possible tags for this assignment
    Output: 
        accuracy: Number of times you classified a word correctly
    '''
    # Initialize the number of correct predictions to zero
    num_correct = 0
    # Get the (tag, word) tuples, stored as a set
    all_words = set(emission_counts.keys())
    # Get the number of (word, POS) tuples in the corpus 'y'
    total = len(y)
    for word, y_tup in zip(prep, y): 
        # Split the (word, POS) string into a list of two items
        y_tup_l = list(y_tup)
        # Verify that y_tup contain both word and POS
        if len(y_tup_l) == 2:
            # Set the true POS label for this word
            true_label = y_tup_l[1]
        else:
            # If the y_tup didn't contain word and POS, go to next word
            continue
        count_final = 0
        pos_final = ''
        # If the word is in the vocabulary...
        if word in vocab:
            for pos in states:
                # define the key as the tuple containing the POS and word
                key = (pos, word)
                # check if the (pos, word) key exists in the emission_counts dictionary
                if key in emission_counts: # Replace None in this line with the proper condition.
                # get the emission count of the (pos,word) tuple 
                    count = emission_counts[key]
                    # keep track of the POS with the largest count
                    if count > count_final: # Replace None in this line with the proper condition.
                        # update the final count (largest count)
                        count_final = count
                        # update the final POS
                        pos_final = pos
            # If the final POS (with the largest count) matches the true POS:
            if pos_final == true_label: # Replace None in this line with the proper condition.
                # Update the number of correct predictions
                num_correct += 1
    accuracy = num_correct / total
    return accuracy


def create_transition_matrix(alpha, tag_counts, transition_counts):
    ''' 
    Input: 
        alpha: number used for smoothing
        tag_counts: a dictionary mapping each tag to its respective count
        transition_counts: a dictionary where the keys are (prev_tag, tag) and the values are the counts
    Output:
        A: matrix of dimension (num_tags,num_tags)
    '''
    # Get a sorted list of unique POS tags
    all_tags = sorted(tag_counts.keys())
    
    # Count the number of unique POS tags
    num_tags = len(all_tags)
    
    # Initialize the transition matrix 'A'
    A = np.zeros((num_tags,num_tags))
    
    # Get the unique transition tuples (previous POS, current POS)
    trans_keys = set(transition_counts.keys())
    
    ### START CODE HERE ### 
    
    # Go through each row of the transition matrix A
    for i in range(num_tags):
        
        # Go through each column of the transition matrix A
        for j in range(num_tags):

            # Initialize the count of the (prev POS, current POS) to zero
            count = 0
        
            # Define the tuple (prev POS, current POS)
            # Get the tag at position i and tag at position j (from the all_tags list)
            key = (all_tags[i], all_tags[j]) # tuple of form (tag,tag)

            # Check if the (prev POS, current POS) tuple 
            # exists in the transition counts dictionary
            if key in transition_counts: # Replace None in this line with the proper condition.
                
                # Get count from the transition_counts dictionary 
                # for the (prev POS, current POS) tuple
                count = transition_counts[key]

            # Get the count of the previous tag (index position i) from tag_counts
            count_prev_tag = tag_counts[key[0]]
            
            # Apply smoothing using count of the tuple, alpha, 
            # count of previous tag, alpha, and total number of tags
            A[i,j] = (count + alpha) / (count_prev_tag + num_tags*alpha)

    ### END CODE HERE ###
    return A

def create_emission_matrix(alpha, tag_counts, emission_counts, vocab):
    '''
    Input: 
        alpha: tuning parameter used in smoothing 
        tag_counts: a dictionary mapping each tag to its respective count
        emission_counts: a dictionary where the keys are (tag, word) and the values are the counts
        vocab: a dictionary where keys are words in vocabulary and value is an index.
               within the function it'll be treated as a list
    Output:
        B: a matrix of dimension (num_tags, len(vocab))
    '''
    # get the number of POS tag
    num_tags = len(tag_counts)
    # Get a list of all POS tags
    all_tags = sorted(tag_counts.keys())
    # Get the total number of unique words in the vocabulary
    num_words = len(vocab)
    # Initialize the emission matrix B with places for
    # tags in the rows and words in the columns
    B = np.zeros((num_tags, num_words))
    # Get a set of all (POS, word) tuples 
    # from the keys of the emission_counts dictionary
    emis_keys = set(list(emission_counts.keys()))
    # Go through each row (POS tags)
    for i in range(0, num_tags): # Replace None in this line with the proper range.
        # Go through each column (words)
        for j in range(0, num_words): # Replace None in this line with the proper range.
            # Initialize the emission count for the (POS tag, word) to zero
            count = 0
            # Define the (POS tag, word) tuple for this row and column
            key = (all_tags[i], vocab[j]) # tuple of form (tag,word)
            # check if the (POS tag, word) tuple exists as a key in emission counts
            if key in emis_keys: # Replace None in this line with the proper condition.
                # Get the count of (POS tag, word) from the emission_counts d
                count = emission_counts[key]
            # Get the count of the POS tag
            count_tag = tag_counts[key[0]]
            # Apply smoothing and store the smoothed value 
            # into the emission matrix B for this row and column
            B[i,j] = (count + alpha) / (count_tag + num_words*alpha)
    return B



def initialize(states, tag_counts, A, B, corpus, vocab):
    '''
    Input: 
        states: a list of all possible parts-of-speech
        tag_counts: a dictionary mapping each tag to its respective count
        A: Transition Matrix of dimension (num_tags, num_tags)
        B: Emission Matrix of dimension (num_tags, len(vocab))
        corpus: a sequence of words whose POS is to be identified in a list 
        vocab: a dictionary where keys are words in vocabulary and value is an index
    Output:
        best_probs: matrix of dimension (num_tags, len(corpus)) of floats
        best_paths: matrix of dimension (num_tags, len(corpus)) of integers
    '''
    # Get the total number of unique POS tags
    num_tags = len(tag_counts)
    # Initialize best_probs matrix 
    # POS tags in the rows, number of words in the corpus as the columns
    best_probs = np.zeros((num_tags, len(corpus)))
    # Initialize best_paths matrix
    # POS tags in the rows, number of words in the corpus as columns
    best_paths = np.zeros((num_tags, len(corpus)), dtype=int)
    # Define the start token
    s_idx = states.index("--s--")
    # Go through each of the POS tags
    for i in range(0, num_tags): # Replace None in this line with the proper range.
        # Handle the special case when the transition from start token to POS tag i is zero
        if A[s_idx, i] == 0: # Replace None in this line with the proper condition. # POS by word
            # Initialize best_probs at POS tag 'i', column 0, to negative infinity
            best_probs[i,0] = float("-inf")
        # For all other cases when transition from start token to POS tag i is non-zero:
        else:
            # Initialize best_probs at POS tag 'i', column 0
            # Check the formula in the instructions above
            best_probs[i,0] = math.log(A[s_idx, i])+math.log(B[i, vocab[corpus[0]]])
    return best_probs, best_paths






def interface(mensaje_comprimido, mensaje_descomprimido):
    dataset = [(tag, word) for tag, word in zip(mensaje_descomprimido, mensaje_comprimido)]

    lim = 10
    training_corpus = dataset[:-lim]
    testing_corpus = dataset[-lim:]
    print(len(training_corpus))
    print(len(testing_corpus))

    # vocab: dictionary that has the index of the corresponding words
    vocab = {}
    # Get the index of the corresponding words.
    for i, word in enumerate(sorted(mensaje_descomprimido)):
        vocab[word] = i

    emission_counts, transition_counts, tag_counts = create_dictionaries(training_corpus, vocab)

    # get all the POS states
    states = sorted(tag_counts.keys())
    print(f"Number of POS tags (number of 'states'): {len(states)}")
    print("View these POS tags (states)")
    print(states)

    accuracy_predict_pos = predict_pos(mensaje_descomprimido[-lim:], testing_corpus, emission_counts, vocab, states)
    print(f"Accuracy of prediction using predict_pos is {accuracy_predict_pos:.4f}")

    alpha = 0.001
    A = create_transition_matrix(alpha, tag_counts, transition_counts)
    B = create_emission_matrix(alpha, tag_counts, emission_counts, list(vocab))

    #print(A)
    
    #print(tag_counts)

    #best_probs, best_paths = initialize(states, tag_counts, A, B, mensaje_descomprimido[-lim:], vocab)



def main() -> None:
    window_size = 12
    lookup_size = 5
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    message = "abbabbaaaabbbabaaaaaabaaaabaababababaaabababbaaabbbbababababbaabbabbbabababbbababaababababababbababababbababbabbabbabbbbaaaababbaaaabbabbabaaaabbbabbbbababbababaabaaaaaaaaaaaaaabbbbabbabababababbabaaaaababbaaabbbbababababbaabbabbbabababbbababaaaaaaaaaaaaabbbbbbbbababbaaabbbbababababbaabbabbbabababbbababbbbbbbbbbbbbbababbbbabababbaa"

    compresor = Compressor(window_size, lookup_size, alphabet)
    mensaje_comprimido = compresor.compress(message, symb='_')
    #print(len(mensaje_comprimido))

    decompresor = Decompressor(window_size, lookup_size, alphabet)
    mensaje_descomprimido = decompresor.decompress(
        mensaje_comprimido, symb='_')
    #print(len(mensaje_descomprimido))

    interface(mensaje_comprimido, mensaje_descomprimido)

    return 0


main()
