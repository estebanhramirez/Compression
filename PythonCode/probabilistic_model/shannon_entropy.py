import numpy as np


def shannon_entropy(previous_n_gram, probability_matrix):
    """
        Input:
        Output:
        Complexity:
        Explanation:
    """

    entropy = 0
    for nxt in probability_matrix.columns:
        conditional_prob = probability_matrix.loc[[previous_n_gram]][nxt][0]
        entropy += conditional_prob*np.log(1/conditional_prob)
    return entropy
