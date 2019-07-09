#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea
"""

#Defines a function which uses a subject's number, loads their EEG data and stimulus sequence and
# optimizes the tau value for their Bayesian Updating iteratively using the bounded Brent-Dekker method, 
# while fitting a simple linear regression at each step

subj = 2
simul = 1

import pandas as pd
from LinearFit import LinearFit

if simul == 1:
    firstlevel = pd.DataFrame(columns=['simufile', 'cost_function', 'tau', 'baysur_slope', 'regr_intercept', 'sigmasqr'])
elif simul == 0:    
    firstlevel = pd.DataFrame(columns=['subject', 'cost_function', 'tau', 'baysur_slope', 'regr_intercept', 'sigmasqr'])



counter = 0

for tau in [5, 8, 12, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]:
    (costfun, ml_lm, sigmasq) = LinearFit(tau, subj, simul)

    firstlevel.loc[counter,:] = [str(subj), costfun, tau, ml_lm.coef_[-1], ml_lm.intercept_, sigmasq]
    
    counter = counter + 1
    
    if simul == 1:
        firstlevel.to_csv("simul_sub" + str(subj) + "_explorvalues_5_10000.csv", sep=";")
    elif simul == 0:
        firstlevel.to_csv("SemSur_sub" + str(subj) + "_explorvalues_5_10000.csv", sep=";")