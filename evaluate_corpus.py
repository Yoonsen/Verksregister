#!/usr/bin/env python
# coding: utf-8

# # Evaluer tidsepoken for en bok

import dhlab.text as dh
import pandas as pd
from scipy.spatial.distance import cosine



def evaluate_corpus_norwegian(corpus=None, matrix=None, top_number=50):
    """corpus is a dh.Corpus, matrix an evaluation matrix with columns corresponding to years, and rows a word weighted for each year"""
    
    # normalize corpus
    corps= corpus.corpus[corpus.corpus['langs'].str.contains('nob')]
    check = dh.Counts(corps)
    
    for x in check.counts:
        check.counts[x] = check.counts[x]/check.counts[x].sum()
        
    # values to be returned
    vals = dict()
    
    # loop through the corpus and evaluate each book against the matrix
    check_df = check.counts
    for x in check_df:
        # sort the book according to frequency and keep the top_number
        targets = check_df.iloc[check_df[x].fillna(0).to_numpy().nonzero()].index
        res = {x:[]}
        for z in matrix:
            
            # check which words are both in the book as well as in the matrix
            
            words = [w for w in matrix[z].sort_values(ascending=False).index if w in targets][:top_number]
            
            # evaluate matrix against book using scipy cosine
            try:
                df = pd.concat([matrix[z].loc[words], check_df[x].loc[words]], axis = 1)
                df.columns = [0, 1]
                res[x].append((z, cosine(df[0], df[1])))
            except ZeroDivisionError:
                pass
        # sort the result and keep the best
        res[x].sort(key= lambda x: x[1], reverse = False)
        vals[x] = res[x][0]
        
    return vals