# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 09:23:19 2020

@author: ashish
"""
import numpy as np
import pandas as pd
import itertools
import csv

import timeit

start = timeit.default_timer()
from datetime import datetime

# current date and time
begin = datetime.now()


def findsubsets(S, m):
    return set(itertools.combinations(S, m))


vocab_nips = pd.read_csv("G:/bagOfWords/vocab.kos.txt", header=None)
docword_nips = pd.read_csv("G:/bagOfWords/docword.kos.txt", header=None, skiprows=3,
                           delimiter='\s', names=['docID', 'wordID', 'count'])

print("line 28")
ls = 0.0003  # lowest minimum support allowed
beta = 0.5

vocab_mod = vocab_nips.copy()
vocab_mod.index = np.arange(1, len(vocab_mod) + 1)
vocab_mod['frequency'] = docword_nips['count'].groupby(docword_nips['wordID']).sum()
vocab_mod.dropna(axis=0, inplace=True)
vocab_mod['wordID'] = vocab_mod.index
# vocab_mod.index = np.arange(1, len(vocab_mod) + 1)
vocab_mod['frequency'] /= docword_nips['count'].sum()
vocab_mod['MI'] = beta * vocab_mod['frequency']
vocab_mod['MIS'] = (vocab_mod['MI'] > ls) * vocab_mod['MI'] + (1 - vocab_mod['MI'] > ls) * ls
vocab_mod.columns = ['word', 'frequency', 'wordID', 'MI', 'MIS']
vocab_mod.sort_values(by='MIS', ascending=True, inplace=True)
vocab_mod.index = np.arange(1, len(vocab_mod) + 1)

print("line 37")

I = vocab_mod['wordID']
M = vocab_mod[['wordID', 'MIS']].sort_values(by='MIS', ascending=True)

L = {}

min_index = vocab_mod[vocab_mod['MIS'] >= ls].index.values.astype(int)[0]
idx = list(vocab_mod.index)
mis = vocab_mod['MIS'].loc[min_index]
print(mis)
F = [vocab_mod['wordID'].loc[min_index]]
for i in idx[min_index + 1:]:
    if vocab_mod['frequency'].loc[i] >= mis:
        F.append(vocab_mod['wordID'].loc[i])
F = F[-300:]
print("Length = ", len(F))
L[1] = []
for word_id in F:
    freq = vocab_mod[vocab_mod['wordID'] == word_id]['frequency'].iloc[0]
    mis = vocab_mod[vocab_mod['wordID'] == word_id]['MIS'].iloc[0]
    if freq >= mis:
        L[1].append((word_id,))

print("line 58")
k = 2
C = {}


def level2_candidate_gen(F):
    C2 = []

    for i in range(len(F)):
        freq = vocab_mod[vocab_mod['wordID'] == F[i]]['frequency'].iloc[0]
        mis = vocab_mod[vocab_mod['wordID'] == F[i]]['MIS'].iloc[0]
        if (freq > mis):
            for j in range(i + 1, len(F)):
                if vocab_mod[vocab_mod['wordID'] == F[j]]['frequency'].iloc[0] > mis:
                    C2.append((F[i], F[j], [0]))
            print(len(C2))
    return C2


def candidate_gen(L, k):
    Ck = []
    count = 0
    for itemset1 in L:  # Lk-1
        mis1 = vocab_mod[vocab_mod['wordID'] == itemset1[-1]]['MIS'].iloc[0]
        for itemset2 in L[count + 1:]:
            mis2 = vocab_mod[vocab_mod['wordID'] == itemset2[-1]]['MIS'].iloc[0]
            if (itemset1[:-1] ==    itemset2[:-1]):
                count += 1
                if (mis1 < mis2):
                    l1 = list(itemset1)
                    l1.append(itemset2[-1])
                    c = tuple(l1)
                    Ck.append((c, [0]))

    for c in Ck:
        k_minus_sub_c = findsubsets(c[:-1], k - 1)
        for sub_set in k_minus_sub_c:
            mis1 = vocab_mod[vocab_mod['wordID'] == c[0]]['MIS'].iloc[0]
            mis1 = vocab_mod[vocab_mod['wordID'] == c[1]]['MIS'].iloc[0]
            if (c[0] in sub_set) or (mis1 == mis2):
                if sub_set not in L:
                    Ck.remove(c)
    return Ck


while (len(L[k - 1]) and k <= 5):
    if k == 2:
        C[k] = level2_candidate_gen(F)
    else:
        C[k] = candidate_gen(L[k - 1], k)
    for i in list(set(docword_nips['docID'].values)):
        tuple_of_words = tuple(docword_nips['wordID'].where(docword_nips['docID'] == i).dropna().astype('int64'))
        for candidates in C[k]:
            if (k > 2):
                if set([element for tupl in candidates[:-1] for element in tupl]).issubset(tuple_of_words):
                    candidates[-1][0] += 1
            else:
                if set(candidates[:-1]).issubset(tuple_of_words):
                    candidates[-1][0] += 1
    L[k] = []
    for candidates in C[k]:
        if (k <= 2):
            if candidates[-1][0] / len(set(docword_nips['docID'])) > \
                    vocab_mod[vocab_mod['wordID'] == candidates[0]]['MIS'].iloc[0]:
                L[k].append(candidates[:-1])
        else:
            if candidates[-1][0] / len(set(docword_nips['docID'])) > \
                    vocab_mod[vocab_mod['wordID'] == candidates[0][0]]['MIS'].iloc[0]:
                L[k].append(candidates[0])

    print("line 126")
    print(len(L[k]))
    k += 1

print("line 130")
itemsets = L.copy()
output = {}
for _k, _v in itemsets.items():
    output[_k] = []
    for item in _v:
        l = []
        for itemset in item:
            l.append(vocab_mod[vocab_mod['wordID'] == itemset]['word'].iloc[0])
        l = tuple(l)
        output[_k].append(l)

print("line 142")
file_name = "output_nips_ls" + str(ls) + "_beta" + str(beta) + ".csv"
w = csv.writer(open(file_name, "w"))
for key, val in output.items():
    w.writerow([key, val])

print("line 148")

stop = timeit.default_timer()
end = datetime.now()
print('Start Time: ', begin,
      'Stop Time: ', end,
      'Time Taken: ', stop - start)
