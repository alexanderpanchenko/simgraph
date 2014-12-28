#!/usr/bin/python
# -!- coding: utf-8 -!-
# usage: semclos.py modelfilename mode{path - weightedpath - pmi} maxpathlength testfilename  outfilename (showpath)
# usage: semclos.py modelfilename mode{path - weightedpath - pmi} maxpathlength testword1 testword2    outfilenam (showpath)
import codecs
import re
import os
import sys
import csv
import nltk
import networkx as nx
import pickle
import cooccurtrain
from cooccurtrain import load_freq_dict
import time
from time import gmtime, strftime
import random



SnowballStemmer = nltk.stem.snowball.RussianStemmer(ignore_stopwords=True)
usage = '''usage: semclos.py modelfilename mode {path - weightedpath - pmi} maxpathlength testfilename outfilename (showpath)'''





def get_sample(fn):
    with codecs.open(fn, 'rb') as infile:
        csv_reader = csv.DictReader(infile, delimiter=',')
        results = {}
        for row in csv_reader:
                w1 = row['word1']
                w3 = unicode(w1, encoding='utf-8', errors='replace')
                w2 = row['word2']
                w4 = unicode(w2, encoding='utf-8', errors='replace')
                sim = row['sim']
                results.update({(w3, w4): sim})
    return results


def lex_sim(word1, word2, stemmer=None):
    st1 = stemmer.stem(word1)
    st2 = stemmer.stem(word2)
    if st1 in st2 or st2 in st1:
        print word1, st1, word2, st2
        return 0.66
    else: return 0.0


def is_connected(word1, word2, graph, mode=None, length=None, show_path=False):
    sim = 0.0
    path = []
    if graph.has_node(word1) and graph.has_node(word2):
        if nx.has_path(graph, word1, word2):
            weight, path = nx.bidirectional_dijkstra(graph, word1, word2, weight='w')
            if 'path' in mode:
                    if len(path) <= length:
                        if mode == 'weightedpath':
                            # sim = ([weight[w]/path_length for weight in weights for w in weight])/len(path)
                            # sim = weight/len(path)
                            sim = weight
                        elif mode == 'inversepath':
                            sim = 1/float(len(path))
            elif mode == 'pmi':
                sim = graph.get_edge_data(word1, word2)
        else:
            sim = lex_sim(word1, word2, stemmer=SnowballStemmer)
    else: sim = 0.0 #random.uniform(0, 1)

    if show_path is True:
        return (sim, path)
    else: return sim



def get_sim(testbunch, G, mode=None, length=None, showpath=False):
    results = {}
    n = 0
    print 'Computing similarity in %s mode...' % mode
    for item in testbunch:
        n+=1
        if n % 1 == 0: print 'Processed %s words at %s \n' % (n, strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
        word1, word2 = item
        if showpath is True:
            sim = is_connected(word1, word2, G, mode, length, show_path=True)
            results.update({item: (testbunch[item], sim)})
        else:
            sim = is_connected(word1, word2, G, mode, length, show_path=False)
            results.update({item: (testbunch[item], sim)})
    return results



def save(outfn, header, res):
    with codecs.open(outfn, 'a', 'utf-8') as outfile:
        outfile.write(separator.join(header) + '\n')
        for i in res:
            sim, t = res[i]
            sim2, path = t
            outfile.write(separator.join(i) + separator + str(sim) + separator + str(sim2)
                         + separator  + str(path) + '\n')

def _test_is_connected(G, word1, word2):
    l = is_connected(G, word1, word2,  mode='pathweigthed', length=8)
    print l


if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print (usage)
        sys.exit()

    G = nx.read_gpickle(sys.argv[1])
    testsamlpe = get_sample(sys.argv[4])
    n = 0
    if sys.argv[6] == 'showpath':
        res = get_sim(testsamlpe, G, mode=sys.argv[2], length=sys.argv[3], showpath=True)
        for i in sorted(res, key=res.get, reverse=True):
            sim, t = res[i]
            sim2, path = t
            if sim2 == 0.0 and sim > 0.09: n+=1
            print ' '.join(i), sim, sim2, ', '.join(path)
        print '%s words without similarity where it should have been' % n
    else:
        res = get_sim(testsamlpe, G, mode=sys.argv[2], length=sys.argv[3], showpath=False)
        for i in sorted(res, key=res.get, reverse=True):
            print ' '.join(i), res[i]
    header = ['word1', 'word2', 'GS', 'sim', 'path']
    separator = ';'
    save(sys.argv[5], header, res)

