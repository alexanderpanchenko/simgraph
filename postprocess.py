#!/usr/bin/python
# -!- coding: utf-8 -!-
# usage: postprocess.py sr resfn1 resfn2 resfn3 outfn

import codecs
import re
import os
import sys
import csv





usage = 'postprocess.py sr resfn1 resfn2 resfn3 outfn\n'

separator = ','



def mean(*args):
    return float(sum(args)/len(args))



def load_results(fn):
    results = {}
    with codecs.open(fn, 'r') as infile:
        for n, item in enumerate(infile):
            if n > 0:
                bigram = ', '.join(item.split(separator)[0:2])
                results[bigram] = {}
                subdict = results[bigram]
                subdict['gs_sim'] = float(item.split(separator)[2])
                subdict['sim'] = float(item.split(separator)[3])
                subdict['path'] = ', '.join(p for p in item.split(separator)[4:] if p != '')
        return results


def get_mean(results1, results2, results3):
    total_results = {}
    max_min = []
    for bigram1 in results1:
        for bigram2 in results2:
            for bigram3 in results3:
                if bigram1 == bigram2 and bigram2 == bigram3:
                    a = results1[bigram1]
                    b = results2[bigram2]
                    c = results3[bigram3]
                    max_min.extend((a['sim'], b['sim'], c['sim']))
                    total_results[bigram1] = [a['gs_sim'], mean(a['sim'], b['sim'], c['sim'])*max(max_min)]
    return total_results




def save(outfn, header, res):
    with codecs.open(outfn, 'wb') as outfile:
        outfile.write(separator.join(header) + '\n')
        for i in res:
            gs_sim, sim = res[i]
            outfile.write(i + separator + str(gs_sim) + separator + str(sim) + '\n')



if(len(sys.argv) < 2):
    print (usage)
    sys.exit()


if __name__ == '__main__':
    if sys.argv[1] == 'sr':
        total_results = get_mean(load_results(sys.argv[2]),
                                 load_results(sys.argv[3]),
                                 load_results(sys.argv[4]))
        for i in total_results:
            gs_sim, sim = total_results[i]
            print i, gs_sim, sim

        header = ['word1', 'word2', 'gs_sim', 'sim']
        save(sys.argv[5], header, total_results)




