#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea
"""

import os
os.chdir(os.path.dirname(__file__))
import pandas as pd
import numpy as np
import time
import math

from LinearFit import LinearFit
from BayesianUpdating import BayesianUpdating



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

interc = np.median(datamedians) # will be used as simulation intercept, because in reality the intercept will not deviate far from the median






################################## Create simulation data for parameter recovery

realvals = pd.DataFrame(columns=['simufile', 'subject', 'real_tau', 'real_slope', 'real_intercept', 'real_sigmasqr'])


counter = 0
coef_array = [[0, 0, 0, 0, -50], [0, 0, 0, 0, -2], [0, 0, 0, 0, 2], [0, 0, 0, 0, 50]] # sets the slopes for the control variables to 0
subj = 1 # which subject's stimulus sequence to use for simulation

for tau in [5,10,15,20,50,100]:
    for bet in range(0,len(coef_array)):
        beta_coefs = coef_array[bet]
        for sigmasq in [0, 1, medvar, meanvar]:
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
            seq_forUpd = seq.drop(['seg', 'badseg', 'meanamp_ROI', 'standard', 'wordreps', 'word.y', 'Typefrequenz_absolut', 'Nachbarn_mittel_absolut', 'Typelaenge_Zeichen'], axis=1)
            
            BayUpdMeasures = BayesianUpdating(seq_forUpd, tau, alpha0, beta0)
            seq_forUpd = seq_forUpd.drop(['baysur', 'prederr'], axis=1)
            
            input_output = seq.merge(BayUpdMeasures, left_index=True, right_index=True, sort=False)
            input_output = input_output[['seg', 'badseg', 'meanamp_ROI', 'standard', 'wordreps', 'word.y', 'Typefrequenz_absolut', 'Nachbarn_mittel_absolut', 'Typelaenge_Zeichen', 'baysur', 'prederr']]
            input_output = input_output.replace([np.inf, -np.inf], np.nan) # remove rows with infinite values for baysur
            maxbs = max(input_output.baysur)
            minbs = min(input_output.baysur)
            input_output.baysur = (input_output.baysur-minbs)/(maxbs-minbs) # re-scales the regressor to its own range
            maxbs = max(input_output.baysur)
            
            X = input_output[['wordreps', 'Typefrequenz_absolut', 'Nachbarn_mittel_absolut', 'Typelaenge_Zeichen', 'baysur']].values
            
            error = np.random.normal(loc=0.0, scale=math.sqrt(sigmasq), size=len(input_output))
            simul_data = np.dot(X, beta_coefs) + interc + error
            
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
            
            realvals.loc[counter,:] = [counter, subj, tau, beta_coefs[-1], interc, sigmasq]
            
            realvals.to_csv('Simudata/simufile_realvals.csv', sep=";")



############################# Try parameter recovery on simulated data
#counter = 96
num_simfiles = counter
recovery = pd.DataFrame(columns=['simufile', 'cost_function', 'tau', 'slope_wordreps', 'slope_Typefrequenz_absolut', 'slope_Nachbarn_mittel_absolut', 'slope_Typelaenge_Zeichen', 'slope_baysur', 'regr_intercept', 'baysur_pval', 'resid_var'])

counter = 0
simul = 1

for subj in range(1,num_simfiles+1):
    for tau in [5,10,15,20,50,100]:
        ols_lm = LinearFit(tau, subj, simul)
    
        recovery.loc[counter,:] = [str(subj), ols_lm.ssr, tau, ols_lm.params.wordreps, ols_lm.params.Typefrequenz_absolut, ols_lm.params.Nachbarn_mittel_absolut, ols_lm.params.Typelaenge_Zeichen, ols_lm.params.baysur, ols_lm.params.Intercept, ols_lm.pvalues.baysur, np.var(ols_lm.resid)]
        
        counter = counter + 1
        
        recovery.to_csv("Simudata/recovery_all_simfiles.csv", sep=";")


############################# Plot recovered parameters
import matplotlib.pyplot as plt  
import seaborn as sns      
        
realvals = pd.read_csv('Simudata/simufile_realvals.csv', sep=";", index_col=0)
recovery = pd.read_csv("Simudata/recovery_all_simfiles.csv", sep=";", index_col=0)

merged = pd.merge(left=realvals, right=recovery, on="simufile")
merged['real_tau'] = merged.apply(lambda row: "realtau=" + str(row.real_tau), axis=1)

recov_noerr = merged[round(merged.real_sigmasqr) == round(0)]
recov_smallerr = merged[round(merged.real_sigmasqr) == round(1)]
recov_mederr = merged[round(merged.real_sigmasqr) == round(medvar)]
recov_meanerr = merged[round(merged.real_sigmasqr) == round(meanvar)]

noerrplot = sns.lineplot(x="tau", y="cost_function", data=recov_noerr, hue='real_tau', style='real_slope', legend="brief")
noerrplot.legend(loc="top left", bbox_to_anchor=(0.5, 0.5), ncol=2)
noerrplot.get_figure().set_size_inches(25, 20)
noerrplot.set_title("Cost function for the Bayesian Surprise model using simulation data with error variance = 0", fontsize = 30)
noerrplot.get_figure().savefig("Simudata/noerr_recovery.jpg")
plt.clf()

smallerrplot = sns.lineplot(x="tau", y="cost_function", data=recov_smallerr, hue='real_tau', style='real_slope', legend="brief")
smallerrplot.legend(loc="top left", bbox_to_anchor=(0.5, 0.5), ncol=2)
smallerrplot.get_figure().set_size_inches(25, 20)
smallerrplot.set_title("Cost function for the Bayesian Surprise model using simulation data with error variance = 1", fontsize = 30)
smallerrplot.get_figure().savefig("Simudata/smallerr_recovery.jpg")
plt.clf()

mederrplot = sns.lineplot(x="tau", y="cost_function", data=recov_mederr, hue='real_tau', style='real_slope', legend="brief")
mederrplot.legend(bbox_to_anchor=(0.15, 0.18), ncol=4)
mederrplot.get_figure().set_size_inches(25, 20)
mederrplot.set_title("Cost function for the Bayesian Surprise model using simulation data with error variance = " + str(round(medvar)), fontsize = 30)
mederrplot.get_figure().savefig("Simudata/medianvar_recovery.jpg")
plt.clf()

meanerrplot = sns.lineplot(x="tau", y="cost_function", data=recov_meanerr, hue='real_tau', style='real_slope', legend="brief")
meanerrplot.legend(bbox_to_anchor=(0.15, 0.18), ncol=4)
meanerrplot.get_figure().set_size_inches(25, 20)
meanerrplot.set_title("Cost function for the Bayesian Surprise model using simulation data with error variance = " + str(round(meanvar)), fontsize = 30)
meanerrplot.get_figure().savefig("Simudata/meanvar_recovery.jpg")
plt.clf()
