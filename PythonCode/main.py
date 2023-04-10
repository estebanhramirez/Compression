from collections import defaultdict

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def find_cooccurrences(txt, half_context):
    unique_symb = list(set(txt))
    cooccurrences = defaultdict(defaultdict)
    for s in unique_symb:
        tmp_dict = defaultdict(int)
        for t in unique_symb:
            tmp_dict[t] = 0
        cooccurrences[s] = tmp_dict

    txt = ['_' for i in range(half_context)] + txt + ['_' for i in range(half_context)]
    for i in range(half_context, len(txt)-half_context):
        if s == '_':
            continue
        else:
            s = txt[i]
            context = txt[(i - half_context):i:i]+txt[(i+1):(i+half_context+1)]
            tmp_dict = cooccurrences[s]
            for j in range(len(context)):
                t = context[j]
                if t == '_':
                    continue
                else:
                    tmp_dict[t] += 1
            cooccurrences[s] = tmp_dict
    return (cooccurrences)

def dict2vect(cooccurrences):
    for s in cooccurrences.keys():
        cooccurrences[s] = list(cooccurrences[s].values())
    return (cooccurrences)

def euclidean_distance(u, v):
    u = np.array(u) 
    #u = u / np.sqrt(np.sum(u**2))
    v = np.array(v)
    #v = v / np.sqrt(np.sum(v**2))
    d = np.linalg.norm(u-v)
    return (d)

def cosine_similarity(u, v):
    u = np.array(u)
    v = np.array(v)
    cos_sim = np.dot(u, v)/(np.linalg.norm(u)*np.linalg.norm(v))
    return (cos_sim)

def run():
    txt = ['a', 'b', 'c', 'd', 'a', 'b', 'c', 'd', 'a', 'b', 'c', 'd', 'a', 'b', 'c', 'd'] # ['a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b'] # ['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'b', 'b'] # ['a', 'a', 'b', 'a', 'a', 'b', 'a', 'a', 'b', 'a', 'a', 'b', 'a', 'a', 'b', 'a', 'a', 'b', 'a', 'a', 'b']
    half_context = len(txt)
    cooccurrences = find_cooccurrences(txt, half_context)
    print(cooccurrences)
    cooccurrences = dict2vect(cooccurrences)
    print(cooccurrences)
    print('half context:', half_context)
    print(euclidean_distance(cooccurrences['a'], cooccurrences['b']))
    print(cosine_similarity(cooccurrences['a'], cooccurrences['b']))

run()