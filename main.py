from datagen import datagen
from freq_itemsets import freq_itemsets
import pickle


def get_frequent(vocab_txt, doc_txt, k, support):
    datagen_ = datagen(vocab_txt, doc_txt)
    items, transactions, mapping = datagen_.get_data()
    freq_itemsets_ = freq_itemsets(transactions, k, support )
    F, T = freq_itemsets_.apriori()
    return F, T, mapping


if __name__ == '__main__':
    vocab_path = 'data/vocab.kos.txt'
    doc_path = 'data/docword.kos.txt'
    k = 3
    support = 0.01
    F, T, map = get_frequent(vocab_path, doc_path, k, support)
    with open('outputs/test_kos.pickle') as f:
        pickle.dump(F, f, protocol=pickle.HIGHEST_PROTOCOL)


