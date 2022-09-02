# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 14:37:29 2018

@author: epinsky
this scripts reads your ticker file (e.g. MSFT.csv) and
constructs a list of lines
"""
import os

ticker='ZNGA'
input_dir = r'C:\Users\Linda\OneDrive - University at Buffalo\Documents\Spring 2022\cs677\week_1_homework\week_1_homework'
ticker_file = os.path.join(input_dir, ticker + '.csv')

try:   
    with open(ticker_file) as f:
        lines = f.read().splitlines()
    print('opened file for ticker: ', ticker)
    """    your code for assignment 1 goes here
    """
    
except Exception as e:
    print(e)
    print('failed to read stock data for ticker: ', ticker)












