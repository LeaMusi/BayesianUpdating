#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea Musiolek
"""

# Defines a function which uses a tau value and a participant's sequence to compute 
# Bayesian Surprise with uniform priors

def LinearFit(tau, subj):
    from BayesianUpdating import BayesianUpdating
    from sklearn.linear_model import LinearRegression
    import numpy as np
    import pandas as pd
    import math
    
    alpha0 = 1
    beta0 = 1
    
    if subj < 10:
        substr = '0' + str(subj)
    else:
        substr = str(subj)
    sub_path = '/Users/ringelblume/Desktop/SemSur/Data/basefile_SemSur_' + substr + ".csv"
    seq = pd.read_csv(sub_path, encoding = 'unicode_escape', sep=" ")
    seq_forUpd = seq.drop(['seg', 'badseg', 'meanamp_ROI', 'word.y'], axis=1)

    BayUpdMeasures = BayesianUpdating(seq_forUpd, tau, alpha0, beta0)
    
    input_output = seq.merge(BayUpdMeasures, left_index=True, right_index=True, sort=False)
    input_output = input_output[['seg', 'badseg', 'meanamp_ROI', 'word.y', 'baysur', 'prederr']]
    input_output = input_output.loc[input_output['badseg'] != 1]
    input_output = input_output.dropna(axis=0, how='any', subset=['meanamp_ROI'], inplace=False)
    
    y = input_output.meanamp_ROI.values
    x = input_output.baysur.values.reshape((-1, 1))
    lm = LinearRegression().fit(x, y)
    resid_sum_sq = np.sum(np.power(y - lm.predict(X=x), 2))
    #sigmasq = np.var(y - lm.predict(X=x))
    #n = len(y)

    #negloglikeli = -1*(-1*(n*math.log(2*np.pi)/2) -1*(n*math.log(sigmasq)/2) -1*resid_sum_sq/(2*sigmasq**2))
    
    return resid_sum_sq, lm