#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Surtuday July 25 09:56:25 2020

@author: suprise_Dr
"""

import pandas as pd
import numpy as np
import yfinance as yf
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib
import networkx as nx

from collections import defaultdict

class Krus:
    #Initialization requires ticker symbol
    def __init__(self, ticker):
        # Enforce capitalization
        ticker = ticker.upper()
        
        # Symbol is used for labeling plots
        self.symbol = ticker

        '''
        You need  stocks > 1 if you have 1 stock you will get an error
        '''
        try:
            stock = yf.Tickers(ticker)
            stockh = stock.history(period="5d")
            #df = pd.DataFrame(stockh["Close"])
            #print(df.head())
        except Exception as e:
            print('Error Retrieving Data.')
            print(e)
            return
            #copy stock as self stock
        self.stock = stockh.copy()
        #turn to dataframe
        self.df = pd.DataFrame(self.stock["Close"]) 

    #test hello world
    def hello(self):
        print('hello world')

        '''
        Compute log return for each share price
        '''
    def logreturn(self):
        result = np.log(self.df)-np.log(self.df.shift(1))
        #print(result)
        return result

    '''
    Compute  Correlation Coefficients among shares
    '''
    def correlation(self):
        #result = pd.DataFrame(self.stock["Close"].astype('float64'))
        result = self.df.corr()
        #print(result.corr())
        #return result
        self.cR = result.copy()
        return result
    
    '''
        Correlation distance normalization resulting to Adjacency Matrix
    '''
    def distance(self):
        #results = sqrt(2(1-corr))
        #results = (2(1-self.cR))
        sub = (2*(np.subtract(1,self.cR)))**0.5
        #print(sub)
        self.distances = sub.copy()
        return sub

    '''
    KRUSKAL(G):
    A = ∅
    For each vertex v ∈ G.V:
    MAKE-SET(v)
    For each edge (u, v) ∈ G.E ordered by increasing order by weight(u, v):
    if FIND-SET(u) ≠ FIND-SET(v):       
    A = A ∪ {(u, v)}
    UNION(u, v)
    return A
    '''

    def kruskal(self):
        #return 0
        #print(self.distances) 
        G = nx.from_pandas_adjacency(self.distances)
        #A = nx.adjacency_matrix(G) 
        #elist = self.distances
        #G.add_nodes_from(self.distances)
        #G.add_weighted_edges_from(elist)
        #T = nx.minimum_spanning_tree(G)
        T = nx.minimum_spanning_tree(G)
        #mst=nx.minimum_spanning_edges(G,data=False)
        #edgelist=list(mst)
        #print(sorted(edgelist))
        print(sorted(T.edges(data=True)))
        #plt.subplot(121)
        plt.figure(figsize=(20, 20))
        nx.draw(T, with_labels=True, font_weight='bold')
        plt.show()
        #print(G)