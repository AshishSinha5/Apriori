# Apriori Algorithm

A simple python implplementation of Apriori Algorithm for frequent item set mining and association rule learning over relational databases and dataframes. <br>
Here I aim to implement an impllroved version of the algorithm i.e. AprioriTID inspired from Agarwal,Srikant et. al. [[1]](#1)

#### Status: Active

## Dataset
UCI Machine Learning Repository Bag of Words Dataset (http://archive.ics.uci.edu/ml/datasets/Bag+of+Words) by David Newman  contains three collection of text documents 
- Enron Emails - It contains data from about 150 users, mostly senior management of Enron.
- NIPS papers - Contains data from paoers appearing in NIPS conference
- KOS blog entries - Data of KAS blog entries, predominantly stored info about political news

## Getting Started 
- Downlowad the data from the link above.
- Clone the repository to your local PC.
- To extract the required data run the following command (see main.py for args help)
<pre><code>
python main.py -d "data/docword.kos.txt" -v "data/vocab.kos.txt" -k 5 -ms 0.25 -o True
</code></pre>

## Inferences
KOS dataset was passed through apriori algorithm multiple times with minimum support of **0.1, 0.2, 0.25 and 0.3** whereas NIPS dataset had minumum support of **0.4, 0.45, 0.5 and 0.6**. <br>
Some of the interesting frequent itemsets in KOS datasets include - {'create', 'democrats', 'war'}, {'bush', 'general', 'republicans', 'split'} whereas NIPS data had {'abstract', 'algorithm', 'approach', 'information', 'neural'} and {'abstract', 'application', 'input', 'set'} with word *abstract* being present in all the frequent itemset which is expected since all the documents of NIPS data contains word *abstract*.
As we kept increasing minimum support and length of itemset both datasets followed a rather characteristic trend in terms of number of frequent itemsets generated and the time taekn to generate those which is shown in the graphs below.

KOS dataset               |  NIPS dataset
:-------------------------:|:-------------------------:
![KOS ITEMSETS](https://github.com/AshishSinha5/apriori/blob/master/plots/kos_itemset.png)  |  ![NIPS ITEMSETS](https://github.com/AshishSinha5/apriori/blob/master/plots/nips_itemset.png)
![KOS TIME](https://github.com/AshishSinha5/apriori/blob/master/plots/kos_time.png) | ![NIPS TIME](https://github.com/AshishSinha5/apriori/blob/master/plots/kos_time.png)


## References
<a id="1">[1]</a> 
Fast algorithms for mining association rules,1994,
Agrawal, Rakesh and Srikant, Ramakrishnan and others
