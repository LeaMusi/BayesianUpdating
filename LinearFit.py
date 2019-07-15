#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea Musiolek
"""

# Defines a function which uses a tau value and a participant's sequence to compute 
# Bayesian Surprise with uniform priors

def LinearFit(tau, subj, simul):
    from BayesianUpdating import BayesianUpdating
    from sklearn.linear_model import LinearRegression
    import numpy as np
    import pandas as pd
    #import math
    
    alpha0 = 1
    beta0 = 1
    
    if subj < 10:
        substr = '0' + str(subj)
    else:
        substr = str(subj)
        
    if simul == 1:
        sub_path = 'Simudata/simufile' + substr + '.csv'
    elif simul == 0:
        sub_path = '/Users/ringelblume/Desktop/SemSur/Data/basefile_SemSur_' + substr + '.csv'
    
    seq = pd.read_csv(sub_path, encoding = 'unicode_escape', sep=" ", index_col=0)
    seq = seq.dropna(axis=0, how='any', subset=['word.y'], inplace=False)
    seq = seq.sort_values('seg')
    seq_forUpd = seq.drop(['seg', 'badseg', 'meanamp_ROI', 'wordreps', 'word.y', 'Typefrequenz_absolut', 'Nachbarn_mittel_absolut', 'Typelaenge_Zeichen'], axis=1)

    BayUpdMeasures = BayesianUpdating(seq_forUpd, tau, alpha0, beta0)
    seq_forUpd = seq_forUpd.drop(['baysur', 'prederr'], axis=1)
    
    input_output = seq.merge(BayUpdMeasures, left_index=True, right_index=True, sort=False)
    input_output = input_output[['seg', 'badseg', 'meanamp_ROI', 'wordreps', 'word.y', 'Typefrequenz_absolut', 'Nachbarn_mittel_absolut', 'Typelaenge_Zeichen', 'baysur', 'prederr']]
    maxbs = max(input_output.baysur)
    minbs = min(input_output.baysur)
    input_output = input_output.replace([np.inf, -np.inf], np.nan).dropna(axis=0, subset=["baysur"], how="any") # remove rows with infinite values for baysur
    input_output.baysur = (input_output.baysur-minbs)/(maxbs-minbs) # re-scales the regressor to its own range
    maxbs = max(input_output.baysur)
    print("maximum of BS = " + str(maxbs))
    input_output = input_output.dropna(axis=0, how='any', subset=['baysur'], inplace=False)
    
    input_output = input_output.loc[input_output['badseg'] != 1]
    input_output = input_output.dropna(axis=0, how='any', subset=['meanamp_ROI'], inplace=False)
    
    y = input_output.meanamp_ROI
    X = input_output[['wordreps', 'Typefrequenz_absolut', 'Nachbarn_mittel_absolut', 'Typelaenge_Zeichen', 'baysur']]
    lm = LinearRegression().fit(X, y)
    #resid_sum_sq = lm._residues (sometimes empty array)
    resid_sum_sq = sum(np.power((y - lm.predict(X=X)),2))
    sigmasq = np.var(y - lm.predict(X=X))
    #n = len(y)

    #negloglikeli = -1*(-1*(n*math.log(2*np.pi)/2) -1*(n*math.log(sigmasq)/2) -1*resid_sum_sq/(2*sigmasq**2))
    
    return resid_sum_sq, lm, sigmasq