#!/usr/bin/python
# -!- coding: utf-8 -!-
# usage: model.py mkg bigramsfilename outgraphfilename newgraph {True - False}
# usage: model.py rmn graphfilename outgraphfilename
import codecs
import re
import os
import sys
import csv
import networkx as nx
import pickle
import cooccurtrain
from cooccurtrain import load_freq_dict
import time
from time import gmtime, strftime
import numpy


usage = ''' usage: model.py mkg bigramsfilename outgraphfilename graph{new | add} \n 
            usage:  model.py rmn graphfilename outgraphfilename 
            '''
       

def convert_bigrams(cooccur_res):
    weighted_bigrams = []
    for bigram in cooccur_res:
        wb = list(bigram)
        wb.append(cooccur_res[bigram])
        weighted_bigrams.append(tuple(wb))
    return weighted_bigrams


def get_graph(weighted_bigrams, mode=None):
    print 'Beginning to build graph at %s' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    if mode == 'new':
        G = nx.Graph()
        if len(G) > 0: G.clear()
    elif mode == 'add':
        G = nx.read_gpickle(sys.argv[2])
    G.add_weighted_edges_from(weighted_bigrams, weight='w')
    print 'Finished to build  graph at %s' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    print nx.info(G)
    return G




def remove_neg_edges(G):
    bunch = [(u, v) for (u, v, d) in G.edges(data=True) if d['w'] < 0]
    G.remove_edges_from(bunch)
    print nx.info(G)
    return G




if(len(sys.argv) < 2):
    print (usage)
    sys.exit()


if __name__ == '__main__':
    if sys.argv[1] == 'mkg':
        print 'Beginning to load graph dict at %s' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        cooccur_res = load_freq_dict(sys.argv[2], 'bigrams')
        G = get_graph(convert_bigrams(cooccur_res), mode=sys.argv[4])
        print 'Beginning to remove negative edges at %s' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        G2 = remove_neg_edges(G)
        print 'Finished to remove negative edges at %s' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        nx.write_gpickle(G2, sys.argv[3])
        print 'All done! at %s' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

    elif sys.argv[1] == 'rmn':
        print 'Beginning to load graph at %s' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        G = nx.read_gpickle(sys.argv[2])
        print 'Beginning to remove negative edges at %s' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        G2 = remove_neg_edges(G)
        print 'Finished to remove negative edges at %s' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        print 'Beginning to save graph at %s' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        nx.write_gpickle(G2, sys.argv[3])
        print 'All done! at %s' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    elif sys.argv[1] == 'rmmin':
        print 'Beginning to load graph at %s' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        G = nx.read_gpickle(sys.argv[2])
        data = 
        print 'Beginning to remove min weight edges at %s' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())









