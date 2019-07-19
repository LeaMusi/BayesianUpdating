#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea
"""

import os
import pandas as pd
import numpy as np
import time
import math
from LinearFit import LinearFit
from BayesianUpdating import BayesianUpdating

os.chdir("/Users/ringelblume/Desktop/GitHub/Bayesian_Modeling/")

################### Get median and mean variances and medians for guidance in creating simulated data

datavars = list()
datamedians = list()

for subj in range(1, 41):
    if subj < 10:
        substr = '0' + str(subj)
    else:
        substr = str(subj)
    sub_path = '/Users/ringelblume/Desktop/SemSur/Data/basefile_SemSur_' + substr + '.csv'
    seq = pd.read_csv(sub_path, encoding = 'unicode_escape', sep=" ", index_col=0)
    data = seq[['meanamp_ROI']]
    datavar = np.var(data)
    datavars.append(datavar.values)
    datamed = np.nanmedian(data)
    datamedians.append(datamed)
    
    
medvar = np.median(datavars) # will be used as simulation sigma sqr, because in reality the error variance will not be much smaller
meanvar = np.mean(datavars) # will be used as simulation sigma sqr, because in reality the error variance will not be much smaller

medmed = np.median(datamedians) # will be used as simulation intercept, because in reality the intercept will not deviate far from the median






################################## Create simulation data for parameter recovery

realvals = pd.DataFrame(columns=['simufile', 'subject', 'real_tau', 'real_slope', 'real_intercept', 'real_sigmasqr'])


counter = 0
coef_array = [[0, 0, 0, 0, -15], [0, 0, 0, 0, -2], [0, 0, 0, 0, 2], [0, 0, 0, 0, 15]] # sets the slopes for the control variables to 0
subj = 1 # which subject's stimulus sequence to use for simulation

for tau in [5,10,15,20,50,100]:
    for bet in range(0,len(coef_array)):
        beta_coefs = coef_array[bet]
        for sigmasq in [1, medvar, meanvar]:
            counter = counter+1
            
            starttime = time.time()
            alpha0 = 1
            beta0 = 1
            
            if subj < 10:
                substr = '0' + str(subj)
            else:
                substr = str(subj)
            sub_path = '/Users/ringelblume/Desktop/SemSur/Data/basefile_SemSur_' + substr + ".csv"
            seq = pd.read_csv(sub_path, encoding = 'unicode_escape', sep=" ", index_col=0)
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
            
            error = np.random.normal(loc=0.0, scale=math.sqrt(sigmasq), size=len(input_output))
            simul_data = np.dot(X, beta_coefs) + medmed + error
            
            if len(seq)==len(X):
                seq[['meanamp_ROI']] = simul_data
            else:
                print('Error - seq file not of same length as input_output file')
            
            if counter < 10:
                coustr = '0' + str(counter)
            else:
                coustr = str(counter)
            seq.to_csv(path_or_buf='Simudata/simufile' + coustr + '.csv', sep=" ", header=True, mode='w')
            
            elapsed = time.time() - starttime
            print(counter, elapsed)
            
            realvals.loc[counter,:] = [counter, subj, tau, beta_coefs[-1], medmed, sigmasq]
            
            realvals.to_csv('Simudata/simufile_realvals.csv', sep=";")



############################# Try parameter recovery on simulated data
num_simfiles = counter
recovery = pd.DataFrame(columns=['simufile', 'cost_function', 'tau', 'baysur_slope', 'regr_intercept', 'sigmasqr'])

counter = 0
simul = 1

for subj in range(1,num_simfiles+1):
    for tau in [5,10,15,20,50,100]:
        (costfun, ml_lm, sigmasq) = LinearFit(tau, subj, simul)
    
        recovery.loc[counter,:] = [str(subj), costfun, tau, ml_lm.coef_[-1], ml_lm.intercept_, sigmasq]
        
        counter = counter + 1
        
        recovery.to_csv("Simudata/recovery_all_simfiles.csv", sep=";")


############################# Plot recovered parameters
#import matplotlib.pyplot as plt  
import seaborn as sns      
        
realvals = pd.read_csv('Simudata/simufile_realvals.csv', sep=";", index_col=0)
recovery = pd.read_csv("Simudata/recovery_all_simfiles.csv", sep=";", index_col=0)

merged = pd.merge(left=realvals, right=recovery, on="simufile")
merged['realparams'] = merged.apply(lambda row: "realtau=" + str(row.real_tau) + "_realslope=" + str(row.real_slope), axis=1)

recov_smallvar = merged[round(merged.sigmasqr) == round(1)]
recov_medvar = merged[round(merged.sigmasqr) == round(medvar)]
recov_meanvar = merged[round(merged.sigmasqr) == round(meanvar)]

smallvarplot = sns.lmplot(x="tau", y="cost_function", data=recov_smallvar, fit_reg=False, hue='realparams', legend=True)
smallvarplot.savefig("Simudata/smallvar_recovery.jpg")

medvarplot = sns.lmplot(x="tau", y="cost_function", data=recov_medvar, fit_reg=False, hue='realparams', legend=True)
medvarplot.savefig("Simudata/medianvar_recovery.jpg")

meanvarplot = sns.lmplot(x="tau", y="cost_function", data=recov_meanvar, fit_reg=False, hue='realparams', legend=True)
meanvarplot.savefig("Simudata/meanvar_recovery.jpg")


