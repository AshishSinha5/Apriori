import numpy as np
import pandas as pd
from tqdm import tqdm
import itertools
import timeit
from datetime import datetime


class datagen:

    def __init__(self, vocab_txt, doc_txt):
        self.vocab = pd.read_csv(vocab_txt, header=None, names=['words'])
        self.doc = pd.read_csv(doc_txt, header=None, skiprows=3, delimiter='\s', names=['docID', 'wordID', 'count'])
        self.transactions = []
        self.items = []
        self.words = []
        self.mapping = {}

    def __get_transactions__(self):
        print("--------------------------------------------------")
        print("Generating Transaction List")
        self.transactions = [list(self.doc[self.doc['docID'] == i]['wordID']) for i in tqdm(self.doc['docID'].unique())]
        print("Done")
        print("--------------------------------------------------")

    def __get_items__(self):
        print("--------------------------------------------------")
        print("Getting Items")
        self.items = list(range(1, len(self.vocab) + 1))
        print("Done")
        print("--------------------------------------------------")

    def get_data(self):
        self.__get_transactions__()
        self.__get_items__()
        self.words = list(self.vocab['words'])
        self.mapping = dict(zip(self.items, self.words))
        return self.items, self.transactions, self.mapping
