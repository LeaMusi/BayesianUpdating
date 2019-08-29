#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea Musiolek
"""
import pandas as pd

for subj in range(1,41):
    if subj < 10:
        substr = '0' + str(subj)
    else:
        substr = str(subj)
    sub_path = '/Users/ringelblume/Desktop/SemSur/Data/basefile_SemSur_' + substr + ".csv"
    seq = pd.read_csv(sub_path, encoding = 'unicode_escape', sep=" ")
    
    print(subj, seq.isnull().sum()["word.y"])