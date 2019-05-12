#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea
"""

#Defines a function which uses 

def LinearFit(tau, seq):
    from BayesianUpdating import BayesianUpdating
    from sklearn.linear_model import LinearRegression
    import numpy as np
    
    alpha0 = 1
    beta0 = 1
    
    seq_input = seq.drop(['seg', 'badseg', 'meanamp_ROI', 'word.y'], axis=1)

    (BayUpdMeasures, seqarray2) = BayesianUpdating(seq_input, tau, alpha0, beta0)
    
    input_output = seq.merge(BayUpdMeasures, left_index=True, right_index=True, sort=False)
    input_output = input_output[['seg', 'badseg', 'meanamp_ROI', 'word.y', 'baysur', 'prederr']]
    input_output = input_output.loc[input_output['badseg'] != 1]
    input_output = input_output.dropna(axis=0, how='any', subset=['meanamp_ROI'], inplace=False)
    
    y = input_output.meanamp_ROI.values
    x = input_output.baysur.values.reshape((-1, 1))
    lm = LinearRegression().fit(x, y)
    resid_sum_sq = np.sum(np.power(y - lm.predict(X=x), 2))
    sigmasq = np.var(y - lm.predict(X=x))
    neglikeli = -1 * (np.exp( -1 * resid_sum_sq / (2 * sigmasq**2)) /(sigmasq * np.sqrt(2 * np.pi)))
    
    return neglikeli