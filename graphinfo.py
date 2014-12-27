#!/usr/bin/python
# -!- coding: utf-8 -!-
# usage: susage: graphinfo.py modelfilename node 
# usage: graphinfo.py minmax graphfilename outgraphfilename
import codecs
import os
import sys
import itertools
import networkx as nx
import pickle
import time
from time import gmtime, strftime
import random
import matplotlib.pyplot as plt
import numpy


usage = '''usage: graphinfo.py modelfilename node \n
            usage: graphinfo.py minmax graphfilename outgraphfilename 
        '''



if(len(sys.argv) < 2):
        print (usage)
        sys.exit()


def get_max_core_nodes(G):
    results = {}
    coreness =  nx.core_number(G)
    cur_core = None
    for core in coreness:
        cur_core = core
        if cur_core not in results:
            results[cur_core] = coreness[core]
        results[cur_core] = coreness[core]
    return results



def get_and_write_edges_info(in_fn, out_fn):
    print 'Beginning to load graph at %s' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    G = nx.read_gpickle(in_fn)
    print 'Beginning to count weights at %s' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    weights = [d[w] for (u, v, d) in G.edges(data=True) for w in d]
    print [d for n, d in enumerate(weights) if n < 10]

    print 'Beginning to count weights at %s' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    w = numpy.array(weights) 
    print 'Finished to count weights %s' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    print 'Beginning to count max and min weights with numpy array at %s' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    print "min, max, sum"
    min_w = w.min()
    max_w = w.max()
    sum_w = w.sum()
    print min_w, max_w, sum_w
    print 'Finished to count max and min weights at %s' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    print "mean, std dev"
    mean = w.mean()
    std = w.std()
    print mean, std

    dict = {}
    dict[in_fn] = {}
    subdict = dict[in_fn] 
    subdict['min'] = min_w
    subdict['max'] = max_w
    subdict['sum'] = sum_w
    subdict['mean'] = mean
    subdict['std'] = std

    print 'Saving results to %s ' % out_fn
    pickle.dump(dict, open(out_fn, 'ab'))



if __name__ == '__main__':
    if sys.argv[1] == 'graphinfo':
        G = nx.read_gpickle(sys.argv[2])
        print 'Degree of a single node: %s ' % (nx.degree(G, u'год'))
        print 'Degree histogramm: %s ' % nx.degree_histogram(G) [0:10]
        print 'Graph density: %s' % nx.density(G)
        print 'Is directed: %s' % nx.is_directed(G)
        coreness =  get_max_core_nodes(G)
        for n, i in enumerate(sorted(coreness, key=coreness.get, reverse=True)):
            if n < 100:
                print 'Core number: %s for node %s ' % (coreness[i], ''.join(i))
        print nx.info(G)
        print 'Average shortest path length: %s ' % nx.average_shortest_path_length(G)
        print 'Graph diameter: %s' % nx.diameter(G)
        print 'Eccentricity: %s' % nx.eccentricity(G, v=u'год')
        # degree_sequence=sorted(nx.degree(G).values(), reverse=True) # degree sequence
        # print "Degree sequence", degree_sequence
        # dmax=max(degree_sequence)


    elif sys.argv[1] == 'minmax':
         get_and_write_edges_info(sys.argv[2], sys.argv[3])


