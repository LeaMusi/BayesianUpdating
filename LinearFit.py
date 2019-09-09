#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea Musiolek
"""

# Defines a function which uses a tau value and a participant's sequence to compute 
# Bayesian Surprise with uniform priors

def LinearFit(tau, subj, simul, final, bins):
    from BayesianUpdating import BayesianUpdating
    import statsmodels.formula.api as smf
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
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
    seq_forUpd = seq.drop(['seg', 'badseg', 'meanamp_ROI', 'standard', 'wordreps', 'word.y', 'Typefrequenz_absolut', 'Nachbarn_mittel_absolut', 'Typelaenge_Zeichen'], axis=1)

    BayUpdMeasures = BayesianUpdating(seq_forUpd, tau, alpha0, beta0)
    seq_forUpd = seq_forUpd.drop(['baysur', 'prederr'], axis=1)
    
    input_output = seq.merge(BayUpdMeasures, left_index=True, right_index=True, sort=False)
    input_output = input_output[['seg', 'badseg', 'meanamp_ROI', 'standard', 'wordreps', 'word.y', 'Typefrequenz_absolut', 'Nachbarn_mittel_absolut', 'Typelaenge_Zeichen', 'baysur', 'prederr']]
    input_output = input_output.replace([np.inf, -np.inf], np.nan).dropna(axis=0, subset=["baysur"], how="any") # remove rows with infinite values for baysur
    
    # Re-scale the regressors to their own range
    maxbs = max(input_output.baysur)
    minbs = min(input_output.baysur)
    input_output.baysur = (input_output.baysur-minbs)/(maxbs-minbs) 
    maxbs = max(input_output.baysur)
    
    maxwr = max(input_output.wordreps)
    minwr = min(input_output.wordreps)
    input_output.wordreps = (input_output.wordreps-minwr)/(maxwr-minwr) 

    maxtf = max(input_output.Typefrequenz_absolut)
    mintf = min(input_output.Typefrequenz_absolut)
    input_output.Typefrequenz_absolut = (input_output.Typefrequenz_absolut-mintf)/(maxtf-mintf)
    
    maxnm = max(input_output.Nachbarn_mittel_absolut)
    minnm = min(input_output.Nachbarn_mittel_absolut)
    input_output.Nachbarn_mittel_absolut = (input_output.Nachbarn_mittel_absolut-minnm)/(maxnm-minnm)
    
    maxtl = max(input_output.Typelaenge_Zeichen)
    mintl = min(input_output.Typelaenge_Zeichen)
    input_output.Typelaenge_Zeichen = (input_output.Typelaenge_Zeichen-mintl)/(maxtl-mintl)
    
    print("maximum of BS = " + str(maxbs) + ", data points after inf removal: " + str(len(input_output)))
    input_output = input_output.dropna(axis=0, how='any', subset=['baysur'], inplace=False)
    if final:
        input_output.to_csv("SemSurSequences/SemSurSequence_" + substr + ".csv", sep=";")
    
    input_output = input_output.loc[input_output['badseg'] != 1]
    input_output = input_output.dropna(axis=0, how='any', subset=['meanamp_ROI'], inplace=False)
    #input_output.sort_values('baysur', axis=0, ascending=True, inplace=True, kind='mergesort')
    #input_output.reset_index(inplace=True)
    
    if bins != 0: # perform parametrical averaging
        borders = list()
        borders.append(0)
        for bin in range(1, bins):
            borders.append(input_output.baysur.quantile(1/bins*bin))
        borders.append(1)
        
        quant1 = 0
        for bin in range(1, bins+1):
            quant2 = borders[bin]
            
            quantmean = np.mean(input_output.baysur.loc[(input_output['baysur'] >= quant1) & (input_output['baysur'] <= quant2)])
            input_output.baysur.loc[(input_output['baysur'] >= quant1) & (input_output['baysur'] <= quant2)] = quantmean
            
            N400mean = np.mean(input_output.meanamp_ROI.loc[(input_output['baysur'] >= quant1) & (input_output['baysur'] <= quant2)])
            input_output.meanamp_ROI.loc[(input_output['baysur'] >= quant1) & (input_output['baysur'] <= quant2)] = N400mean
            
            quant1 = quant2

            
        #input_output['baysur'].value_counts()  
        #input_output['meanamp_ROI'].value_counts()  
        
        #input_output.baysur.loc[(input_output['baysur'] > borders[1]) & (input_output['baysur'] < borders[-2])] = np.nan
        #input_output = input_output.dropna(axis=0, how='any', subset=['baysur'], inplace=False)
        #input_output.baysur.loc[(input_output['baysur'] < borders[1])] = 0
        #input_output.baysur.loc[(input_output['baysur'] > borders[1])] = 1
    
    #plt.scatter(input_output.baysur, input_output.meanamp_ROI, alpha=0.5)
    #plt.title('Scatter plot for tau = '+str(tau))
    #plt.savefig("Scatterplotsub="+substr+"tau="+str(tau)+".jpg")
    #plt.clf()
    
    results = smf.ols('meanamp_ROI ~ baysur + wordreps + Typefrequenz_absolut + Nachbarn_mittel_absolut + Typelaenge_Zeichen', data=input_output).fit()

    #negloglikeli = -1*(-1*(n*math.log(2*np.pi)/2) -1*(n*math.log(sigmasq)/2) -1*resid_sum_sq/(2*sigmasq**2))
    
    return results