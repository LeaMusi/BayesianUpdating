#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea
"""

import os
import pandas as pd
import math
from BayesianUpdating import BayesianUpdating

os.chdir("/Users/ringelblume/Desktop/GitHub/Bayesian_Modeling/")


#FirstLevel = FirstLevelFit(subj=1, init_tau=30, iters=5)

subj = 1


if subj < 10:
    substr = '0' + str(subj)
else:
    substr = str(subj)
sub_path = '/Users/ringelblume/Desktop/SemSur/Data/basefile_SemSur_' + substr + ".csv"

seq = pd.read_csv(sub_path, encoding = 'unicode_escape', sep=" ")
seq_input = seq.drop(['seg', 'badseg', 'meanamp_ROI', 'word.y'], axis=1)  
input_output = seq[['seg', 'badseg', 'meanamp_ROI', 'word.y']]  

alpha0 = 1
beta0 = 1
tau = 5

for tau in range(2, 6, 2):
    print(tau)
    BayUpdMeasures = BayesianUpdating(seq_input, tau, alpha0, beta0)
    
    BayUpdMeasures = BayUpdMeasures[['baysur']]
    input_output = input_output.merge(BayUpdMeasures, left_index=True, right_index=True, sort=False)
    #input_output = input_output.loc[input_output['badseg'] != 1]
    #input_output = input_output.dropna(axis=0, how='any', subset=['meanamp_ROI'], inplace=False)