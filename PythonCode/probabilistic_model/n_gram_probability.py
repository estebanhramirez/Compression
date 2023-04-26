def n_gram_probability(n_gram, n_gram_counts):
    prob = n_gram_counts[n_gram] / sum(n_gram_counts.values())
    return prob
