"""
    Author: Esteban Hernandez Ramirez
"""


def count_n_grams(data, n, start_token='<s>', end_token='<e>'):
    """
    Input:
        data: [str array array] sentences collection
        n: [int] number of words in a sequence
    Output:
        n_grams: [dictionary (str -> float)] 
    Complexity:
        time: O(n)
        storage: O(n)
    Explanation:
        Count all n-grams in the data. Code adapted
        from Coursera NLP especialization - Course 2
        by 'DeepLearning.AI'.
    """

    # Initialize dictionary of n-grams and their counts
    n_grams = {}

    # Go through each sentence in the data
    for sentence in data:

        # prepend start token n times, and  append the end token one time
        sentence = [start_token for i in range(0, n)] + sentence + [end_token]

        # convert list to tuple
        # So that the sequence of words can be used as
        # a key in the dictionary
        sentence = tuple(sentence)

        # Use 'i' to indicate the start of the n-gram
        # from index 0
        # to the last index where the end of the n-gram
        # is within the sentence.

        for i in range(0, len(sentence)-n+1):

            # Get the n-gram from i to i+n
            n_gram = sentence[i:i+n]

            # check if the n-gram is in the dictionary
            if n_gram in n_grams:

                # Increment the count for this n-gram
                n_grams[n_gram] += 1
            else:
                # Initialize this n-gram count to 1
                n_grams[n_gram] = 1

    return n_grams


def run():
    """
    Input:
        None
    Output:
        None
    Complexity:
        time: O(n)
        storage: O(n)
    """

    sentences = [['a', 'a', 'b', 'a', 'b', 'b', 'b', 'b', 'a', 'a', 'b', 'a', 'b']]
    print("Uni-gram:")
    print(count_n_grams(sentences, 1))
    print("Bi-gram:")
    print(count_n_grams(sentences, 2))
    print("Tri-gram:")
    print(count_n_grams(sentences, 3))


#run()
