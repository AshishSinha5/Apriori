from datagen import datagen
from freq_itemsets import freq_itemsets
import pickle
import argparse


def get_frequent(vocab_txt, doc_txt, k, support):
    datagen_ = datagen(vocab_txt, doc_txt)
    items, transactions, mapping = datagen_.get_data()
    freq_itemsets_ = freq_itemsets(transactions, k, support)
    F, T = freq_itemsets_.apriori()
    return F, T, mapping


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--doc_file_path", help="File path to transactions/docs", default="data/docword.kos.txt",
                        type=str)
    parser.add_argument("-v", "--vocab_file_path", help="File path to vocabulary", default="data/vocab.kos.txt",
                        type=str)
    parser.add_argument("-ms", "--min_support", help="Minimum support", default=0.01, type=float)
    parser.add_argument("-k", "--max_k", help="Max length of itemset", default=3, type=int)
    parser.add_argument("-o", "--save_op", help="Save output", default=False, type=bool)

    args = parser.parse_args()
    doc_path = args.doc_file_path
    vocab_path = args.vocab_file_path
    support = args.min_support
    k = args.max_k
    F, T, map = get_frequent(vocab_path, doc_path, k, support)
    if args.save_op:
        with open('outputs/{}_{}_{}.pickle'.format(doc_path[5:-3], support, k), 'wb') as f:
            pickle.dump(F, f, protocol=pickle.HIGHEST_PROTOCOL)
        with open('outputs/{}_{}_{}_time.pickle'.format(doc_path[5:-3],support, k), 'wb') as f:
            pickle.dump(T, f, protocol=pickle.HIGHEST_PROTOCOL)
