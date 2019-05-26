#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from BayesianUpdating import BayesianUpdating

os.chdir("/Users/ringelblume/Desktop/GitHub/Bayesian_Modeling/")

taurange = np.array([5,10,15,20,25,30,35,40])
subj = 1
ntrials = 200 # Set number of example trials to be used for plotting
alpha0 = 1 # Set uniform priors
beta0 = 1

if subj < 10:
    substr = '0' + str(subj)
else:
    substr = str(subj)
sub_path = '/Users/ringelblume/Desktop/SemSur/Data/basefile_SemSur_' + substr + ".csv"

seq = pd.read_csv(sub_path, encoding = 'unicode_escape', sep=" ")
seq = seq.loc[1:ntrials, :]

input_output = seq[['seg', 'badseg', 'meanamp_ROI', 'word.y']]  




# Compute Bayesian Surprise regressors for different tau values
for tau in taurange:
    print(tau)
    seq_forUpd = seq.drop(['seg', 'badseg', 'meanamp_ROI', 'word.y'], axis=1) # has to be done here, because otherwise next line modifies this object
    BayUpdMeasures = BayesianUpdating(seq_forUpd, tau, alpha0, beta0)
    BayUpdMeasures = BayUpdMeasures[['baysur']]
    BayUpdMeasures.columns = ['baysur_tau_'+str(tau)]
    input_output = input_output.merge(BayUpdMeasures, left_index=True, right_index=True, sort=False)


# Plot the different regressors

forplot = input_output
 
# multiple line plot
num=0
for column in forplot.drop(['seg', 'badseg', 'meanamp_ROI', 'word.y'], axis=1):
    num+=1
    plt.plot(forplot['seg'], forplot[column], marker='', linewidth=0.3, alpha=0.9, label=column)
 
plt.legend(loc=2, ncol=2) # Add legend
# Add titles
plt.title("BS by tau values", loc='center', fontsize=12, fontweight=0, color='black')
plt.xlabel("Trial")
plt.ylabel("Bayesian Surprise")
plt.savefig('regressorplot.png', dpi=400)
