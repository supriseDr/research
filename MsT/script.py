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


class Kruskal(object):

    def __init__(self, ticker):
        """Receives data from yfinance

        Args:
            ticker: The list of the stock ticker symbols
        """
        self.symbol = ticker
        '#force capitalization for tickers'
        ticker = ticker.upper()

        '#Get data from yfinance/yahoo finance from live service'
        try:
            stockData = yf.Tickers(ticker)
            stockHistory = stockData.history(period="30d")
        except Exception as e:
            print('Error Retrieving Data.')
            print(e)
            return
        self.stock = stockHistory.copy()
        self.df = pd.DataFrame(self.stock["Close"])

    def logreturn(self):
        """Method for computing logreturns"""
        logReturns = np.log(self.df)-np.log(self.df.shift(1))
        return logReturns

    def correlation(self):
        """Method for computing correlation from"""
        result = self.df.corr()
        self.cR = result.copy()
        return result

    def distance(self):
        """Converts the Correlations to distances"""
        sub = np.sqrt(2*(np.subtract(1, self.cR)))
        self.distances = sub.copy()
        return sub

    def kruskal(self):
        """Implements the Kruskal algorithm built in nx library"""
        G = nx.from_pandas_adjacency(self.distances)
        T = nx.minimum_spanning_tree(G)
        print(sorted(T.edges(data=True)))
        plt.figure(figsize=(20, 20))
        nx.draw(T, with_labels=True, font_weight='bold')
        plt.show()
