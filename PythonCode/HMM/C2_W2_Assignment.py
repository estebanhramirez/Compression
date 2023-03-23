# Importing packages and loading in the data set 
from utils_pos import get_word_tag, preprocess  
import pandas as pd
from collections import defaultdict
import math
import numpy as np


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
    emission_counts = defaultdict(int)
    transition_counts = defaultdict(int)
    tag_counts = defaultdict(int)
    
    prev_tag = '--s--' 
    
    i = 0 
    
    for word_tag in training_corpus:
        i += 1
        word, tag = get_word_tag(word_tag, vocab)

        transition_counts[(prev_tag, tag)] += 1
        emission_counts[(tag, word)] += 1
        tag_counts[tag] += 1

        prev_tag = tag

    return emission_counts, transition_counts, tag_counts


def create_transition_matrix(alpha, tag_counts, transition_counts):
    ''' 
    Input: 
        alpha: number used for smoothing
        tag_counts: a dictionary mapping each tag to its respective count
        transition_counts: a dictionary where the keys are (prev_tag, tag) and the values are the counts
    Output:
        A: matrix of dimension (num_tags, num_tags)
    '''
    all_tags = sorted(tag_counts.keys())
    num_tags = len(all_tags)

    A = np.zeros((num_tags,num_tags))

    trans_keys = set(transition_counts.keys())

    for i in range(num_tags):
        for j in range(num_tags):
            count = 0
            key = (all_tags[i], all_tags[j])

            if key in trans_keys:
                count = transition_counts[key]

            count_prev_tag = tag_counts[key[0]]

            A[i,j] = (count + alpha) / (count_prev_tag + num_tags*alpha)

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
    num_tags = len(tag_counts)
    all_tags = sorted(tag_counts.keys())
    num_words = len(vocab)

    B = np.zeros((num_tags, num_words))

    emis_keys = set(list(emission_counts.keys()))

    for i in range(0, num_tags):
        for j in range(0, num_words):
            count = 0
            key = (all_tags[i], vocab[j])

            if key in emis_keys:
                count = emission_counts[key]

            count_tag = tag_counts[key[0]]

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
    num_tags = len(tag_counts)

    best_probs = np.zeros((num_tags, len(corpus)))
    best_paths = np.zeros((num_tags, len(corpus)), dtype=int)

    s_idx = states.index("--s--")

    for i in range(0, num_tags):
        if A[s_idx, i] == 0:
            best_probs[i,0] = float("-inf")
        else:
            best_probs[i,0] = math.log(A[s_idx, i])+math.log(B[i, vocab[corpus[0]]])

    return best_probs, best_paths


def viterbi_forward(A, B, test_corpus, best_probs, best_paths, vocab):
    '''
    Input: 
        A, B: The transition and emission matrices respectively
        test_corpus: a list containing a preprocessed corpus
        best_probs: an initilized matrix of dimension (num_tags, len(corpus))
        best_paths: an initilized matrix of dimension (num_tags, len(corpus))
        vocab: a dictionary where keys are words in vocabulary and value is an index 
    Output: 
        best_probs: a completed matrix of dimension (num_tags, len(corpus))
        best_paths: a completed matrix of dimension (num_tags, len(corpus))
    '''
    num_tags = best_probs.shape[0]

    for i in range(1, len(test_corpus)):
        for j in range(0, num_tags):
            best_prob_i = float("-inf")
            best_path_i = None
            for k in range(0, num_tags):
                prob = best_probs[k, i-1] + math.log(A[k, j]) + math.log(B[j, vocab[test_corpus[i]]])

                if prob > best_prob_i:
                    best_prob_i = prob
                    best_path_i = k

            best_probs[j,i] = best_prob_i
            best_paths[j,i] = best_path_i

    return best_probs, best_paths


def viterbi_backward(best_probs, best_paths, corpus, states):
    '''
    This function returns the best path.
    '''
    m = best_paths.shape[1]
    z = [None] * m

    num_tags = best_probs.shape[0]
    best_prob_for_last_word = float('-inf')

    pred = [None] * m
    for k in range(0, num_tags):
        if best_probs[k, m-1] > best_prob_for_last_word:
            best_prob_for_last_word = best_probs[k, m-1]
            z[m - 1] = k

    pred[m - 1] = states[z[m-1]]

    for i in range(m-1, 0, -1):
        pos_tag_for_word_i = z[i]
        z[i - 1] = best_paths[pos_tag_for_word_i, i]
        pred[i - 1] = states[z[i-1]]
    return pred


def compute_accuracy(pred, y):
    '''
    Input: 
        pred: a list of the predicted parts-of-speech 
        y: a list of lines where each word is separated by a '\t' (i.e. word \t tag)
    Output: 
    '''
    num_correct = 0
    total = 0
    for prediction, y in zip(pred, y):
        word_tag_tuple = y.split('~')

        if len(word_tag_tuple) != 2:
            continue

        word, tag = word_tag_tuple

        if prediction == tag:
            num_correct += 1

        total += 1

    accuracy = num_correct/total
    return accuracy


def run():
    # load in the training corpus
    with open("./data/WSJ_02-21.pos", 'r') as f:
        training_corpus = f.readlines()
    lines = training_corpus

    words = [line.split('~')[0] for line in lines]
    freq = defaultdict(int)

    for word in words:
        freq[word] += 1

    vocab = [k for k, v in freq.items() if (v > 1 and k != '\n')] + ['--n--', '--unk--', '--unk_digit--', '--unk_punct--', '--unk_upper--', '--unk_noun--', '--unk_verb--', '--unk_adj--', '--unk_adv--']
    vocab.sort()

    with open('data/hmm_vocab.txt', 'w') as f:
        for word in vocab:
            f.write(word+'\n')

    # read the vocabulary data, split by each line of text, and save the list
    with open("./data/hmm_vocab.txt", 'r') as f:
        voc_l = f.read().split('\n')

    # vocab: dictionary that has the index of the corresponding words
    vocab = {}

    # Get the index of the corresponding words. 
    for i, word in enumerate(sorted(voc_l)): 
        vocab[word] = i
    print("vocab")
    print(vocab)

    #print(training_corpus)
    emission_counts, transition_counts, tag_counts = create_dictionaries(training_corpus, vocab)
    

    # get all the POS states
    states = sorted(tag_counts.keys())
    print(f"Number of POS tags (number of 'states'): {len(states)}")
    print("View these POS tags (states)")
    print(states)

    print("transition examples: ")
    for ex in list(transition_counts.items())[:2]:
        print(ex)
    print()

    print("emission examples: ")
    for ex in list(emission_counts.items())[:2]:
        print (ex)


    # load in the test corpus
    with open("./data/WSJ_24.pos", 'r') as f:
        y = f.readlines()


    words_y = [yi.split('~')[0] for yi in y]
    with open('data/test.words', 'w') as f:
        for word_y in words_y:
            f.write(word_y+'\n')

    #corpus without tags, preprocessed
    _, prep = preprocess(vocab, "./data/test.words")

    print("transition examples: ")
    for ex in list(transition_counts.items())[:3]:
        print(ex)
    print()

    print("emission examples: ")
    for ex in list(emission_counts.items())[200:203]:
        print (ex)
    print()

    alpha = 0.001
    A = create_transition_matrix(alpha, tag_counts, transition_counts)
    B = create_emission_matrix(alpha, tag_counts, emission_counts, list(vocab))


    print(A)
    print(B)

    print("prep")
    print(prep)

    best_probs, best_paths = initialize(states, tag_counts, A, B, prep, vocab)
    best_probs, best_paths = viterbi_forward(A, B, prep, best_probs, best_paths, vocab)
    print(best_probs)
    pred = viterbi_backward(best_probs, best_paths, prep, states)
    print(pred)
    print(f"Accuracy of the Viterbi algorithm is {compute_accuracy(pred, y):.4f}")



run()