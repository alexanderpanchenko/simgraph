#!/usr/bin/python
# -!- coding: utf-8 -!-
# usage: cooccur-filename freq-dict-filename outfilename

import codecs
import re
import os
import sys
import csv
import xml.etree.ElementTree as etree
import time
from time import gmtime, strftime
import math

separator = ';'

usage = 'usage: cooccur-filename freq-dict-filename outfilename'

all_bigrams_freq = 6977919247
all_unigrams_freq = 75854872




def pmi(bigram, unigram_freq_dict, unigram_freq, bigram_freq_dict, bigram_freq):
    word1, word2 = bigram
    prob_word1 = unigram_freq_dict[word1] / float(unigram_freq)
    prob_word2 = unigram_freq_dict[word2] / float(unigram_freq)
    prob_word1_word2 = bigram_freq_dict[bigram] / float(bigram_freq)
    return math.log(prob_word1_word2/float(prob_word1*prob_word2), 2)


def compute_pmi(cooccur_res, unigram_freq_dict, pmi, unigram_freq, bigram_freq_dict, bigram_freq):
    results = {}
    for n, bigram in enumerate(cooccur_res):
        if n % 100000 == 0:
            t = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
            print 'Processed %s bigrams at %s' % (n, t)
        p = pmi(bigram, unigram_freq_dict, unigram_freq, bigram_freq_dict, bigram_freq)
        results.update({bigram: p})
    t = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    print 'Processed %s bigrams at %s' % (len(results), t)
    return results


def load_freq_dict(fn, mode=None):
    results = {}
    with codecs.open(fn, 'r', 'utf-8') as infile:
        for item in infile:
                    t = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
                    if len(results) % 100000 == 0:
                        print 'Loaded %s items from %s at %s' % (len(results), fn, t)
                    if mode == 'unigrams':
                        if item != '':
                            word, freq = item.split(';')
                            results.update({word: int(freq)})
                    elif mode == 'bigrams':
                        if item != '':
                            if ';' in item:
                                bigram = item.split(';')[0:2]
                                freq = item.split(';')[2]
                            else:
                                bigram = item.split()[0:2]
                                freq = item.split()[2]
                            results.update({tuple(bigram): float(freq)})
    return results


def save(outfn, results):
    with codecs.open(outfn, 'a', 'utf-8') as outfile:
        t = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        print 'Beginning to save results to file %s at %s ' % (outfn, t)
        for item in results:
            outfile.write(';'.join(item) + ';' + str(results[item]) + '\n')
    t2 = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    print 'All done at %s' % t2



if __name__ == '__main__':
    if(len(sys.argv) < 3):
        print (usage)
        sys.exit()

    cooccur_res = load_freq_dict(sys.argv[1], 'bigrams')
    unigram_freq_dict = load_freq_dict(sys.argv[2], 'unigrams')
    cooccur_pmi = compute_pmi(cooccur_res, unigram_freq_dict, pmi, all_unigrams_freq, cooccur_res, all_bigrams_freq)
    save(sys.argv[3], cooccur_pmi)







