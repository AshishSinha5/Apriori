import itertools
from tqdm import tqdm
from time import time
import json
from ast import literal_eval
import gc


def is_infrequent(candidate, L_prev) -> bool:
    subsets = itertools.combinations(candidate, len(candidate) - 1)
    for subset in subsets:
        if subset not in L_prev:
            return True
    return False


class freq_itemsets:

    def __init__(self, transaction_list: list, max_k: int, min_sup: float):
        self.transaction_list = transaction_list
        self.max_k = max_k
        self.min_sup = min_sup
        self.min_sup_count = self.min_sup * len(self.transaction_list)
        self.L = {}
        self.Time = []

    def candidate_gen(self, k):
        with open('ck.json', 'w') as f:
            for item1, TID1 in tqdm(self.L[k - 1].items()):
                for item2, TID2 in self.L[k - 1].items():
                    if item1[:-1] == item2[:-1] and item1[-1] < item2[-1]:
                        item_gen = tuple([*item1, item2[-1]])
                        if is_infrequent(item_gen, self.L[k - 1]):
                            continue
                        tid_gen = TID1.intersection(TID2)
                        if tid_gen:
                            ck = {str(item_gen): str(tid_gen)}
                            f.write(json.dumps(ck))
                            f.write('\n')

    def gen_L1(self):
        L1 = {}
        for TID, transaction in enumerate(self.transaction_list):
            for item in transaction:
                if (item,) not in L1:
                    L1[(item,)] = set()
                L1[(item,)].add(TID + 1)
        L1 = {item: TIDs for item, TIDs in L1.items() if len(TIDs) >= self.min_sup_count}
        return L1

    def gen_Lk(self):
        Lk = {}
        with open('ck.json', 'r') as f:
            for line in tqdm(f):
                dict_obj = json.loads(line)
                d = {literal_eval(k): literal_eval(v) for k, v in dict_obj.items()}
                for c, TIDs in d.items():
                    if len(TIDs) < self.min_sup_count:
                        continue
                    Lk[c] = TIDs
        return Lk

    def apriori(self):
        s = time()
        print("--------------------------------------------------")
        print("Generating Frequent Itemsets of Size 1")
        L1 = self.gen_L1()
        self.Time.append(time() - s)
        print("Done")
        print("--------------------------------------------------")
        self.L = {1: L1}
        k = 2
        while k <= self.max_k and self.L[k - 1] is not None:
            s = time()
            print("--------------------------------------------------")
            print("Generating Frequent Item-sets of Size {}".format(k))
            print("Generating Candidates")
            self.candidate_gen(k)
            print("Generating Large Itemsets")
            self.L[k] = self.gen_Lk()
            self.Time.append(time() - s)
            print("Done")
            print("--------------------------------------------------")
            k += 1
        if k > self.max_k:
            print("Maximum required length of {} achieved, exiting".format(self.max_k))
        else:
            print("No frequent itemsets of size {} present, exiting".format(k - 1))
        return self.L, self.Time
