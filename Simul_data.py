#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea Musiolek
"""

# Defines a function which uses a tau value and a participant's sequence to compute 
# Bayesian Surprise with uniform priors

import os
os.chdir("/Users/ringelblume/Desktop/GitHub/Bayesian_Modeling/")
from BayesianUpdating import BayesianUpdating
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import math



subj=1
tau=20
beta_coefs=[1.5, 2, 3, -1, -2]
intercept = 4
sigmasq = 5

alpha0 = 1
beta0 = 1

if subj < 10:
    substr = '0' + str(subj)
else:
    substr = str(subj)
sub_path = '/Users/ringelblume/Desktop/SemSur/Data/basefile_SemSur_' + substr + ".csv"
seq = pd.read_csv(sub_path, encoding = 'unicode_escape', sep=" ")
seq = seq.dropna(axis=0, how='any', subset=['word.y'], inplace=False)
seq = seq.sort_values('seg')
seq[['meanamp_ROI']] = 0
seq_forUpd = seq.drop(['seg', 'badseg', 'meanamp_ROI', 'wordreps', 'word.y', 'Typefrequenz_absolut', 'Nachbarn_mittel_absolut', 'Typelaenge_Zeichen'], axis=1)

BayUpdMeasures = BayesianUpdating(seq_forUpd, tau, alpha0, beta0)
seq_forUpd = seq_forUpd.drop(['baysur', 'prederr'], axis=1)

input_output = seq.merge(BayUpdMeasures, left_index=True, right_index=True, sort=False)
input_output = input_output[['seg', 'badseg', 'meanamp_ROI', 'wordreps', 'word.y', 'Typefrequenz_absolut', 'Nachbarn_mittel_absolut', 'Typelaenge_Zeichen', 'baysur', 'prederr']]
maxbs = max(input_output.baysur)
minbs = min(input_output.baysur)
input_output.baysur = (input_output.baysur-minbs)/(maxbs-minbs)


X = input_output[['wordreps', 'Typefrequenz_absolut', 'Nachbarn_mittel_absolut', 'Typelaenge_Zeichen', 'baysur']].values

simul_data = np.dot(X, beta_coefs) + intercept + np.random.normal(loc=0.0, scale=math.sqrt(sigmasq), size=len(input_output))

if len(seq)==len(input_output):
    seq[['meanamp_ROI']] = simul_data
else:
    print('Error - seq file not of same length as input_output file')

seq.to_csv(path_or_buf='/Users/ringelblume/Desktop/SemSur/Data/simufile_SemSur_' + substr + ".csv", sep=" ", header=True, index=True, index_label=None, mode='w')

#simufile = pd.read_csv(sub_path, encoding = 'unicode_escape', sep=" ")

