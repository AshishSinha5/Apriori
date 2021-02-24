from datagen import datagen
from freq_itemsets import freq_itemsets
from tqdm import tqdm
import pickle


def map_f(F, mapping):
    def map_(i):
        return mapping[i]

    F_mapped = {}
    for i, f in tqdm(tqdm(F.items())):
        F_mapped[i] = []
        for item_set, TIDs in f.items():
            F_mapped[i].append(set(map(map_, item_set)))
    return F_mapped


min_sup = [0.4, 0.45, 0.5, 0.6]
k = 5
data = ['kos', 'nips']
docs = ['data/docword.nips.txt']
vocab = ['data/vocab.nips.txt']

for d, v in zip(docs, vocab):
    datagen_ = datagen(v, d)
    items, transactions, mapping = datagen_.get_data()
    for ms in min_sup:
        freq_itemsets_ = freq_itemsets(transactions, k, ms)
        F, T = freq_itemsets_.apriori()
        F_map = map_f(F, mapping)
        with open('outputs/{}_{}_{}.pickle'.format(d[5:-3], ms, k), 'wb') as f:
            pickle.dump(F, f, protocol=pickle.HIGHEST_PROTOCOL)
        with open('outputs/{}_{}_{}_time.pickle'.format(d[5:-3], ms, k), 'wb') as f:
            pickle.dump(T, f, protocol=pickle.HIGHEST_PROTOCOL)
        with open('outputs/{}_{}_{}_mapped.pickle'.format(d[5:-3], ms, k), 'wb') as f:
            pickle.dump(F_map, f, protocol=pickle.HIGHEST_PROTOCOL)
        del F
        del T
        del F_map
