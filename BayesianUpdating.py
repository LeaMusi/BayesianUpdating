#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea Musiolek
"""

# Defines a Bayesian updating scheme as a function
# Input arguments:
#   seq_input: A pandas data frame containing feature occurrences (results of Bernoulli processes,
#       with columns representing features/Bernoulli processes and rows representing trials)
#   tau: Parameter determining the steepness of the exponential forgetting mechanism for past trials
#   alpha0: Initial prior alpha value for the Bayesian updating on each feature/Bernoulli process
#   beta0: Initial prior beta value for the Bayesian updating on each feature/Bernoulli process


def BayesianUpdating(seq_input, tau, alpha0, beta0):
    #import pandas as pd
    import numpy as np
    #np.seterr(all='ignore')
    import math
    from KL_dirichlet import divergence
    #import matplotlib
    #import matplotlib.pyplot as plt
    #from kl_dirichlet_alt import divergence
    #from simple_difference import divergence
    
    seqarray = seq_input.values # create array out of data frame for better computations
    seqarray2 = seq_input.values # create extra array for temporary storing of alphas
    seqarray2 = np.c_[ seqarray2, np.zeros(np.size(seqarray2,0))] # create extra column for total alpha+beta values
    #features = list(seq_input.dtypes.index)[0:len(seq_input.columns)]
    #newheads = [s + '_alphapost' for s in features]
    #seq_input = pd.concat([seq_input,pd.DataFrame(columns=newheads)], sort=False)
    #seq_input['whole'] = np.NaN
    seq_input['baysur'] = np.NaN  
    seq_input['prederr'] = np.NaN
    
    # Compute Bayesian updating for first trial using a prior based on alpha0 and beta0
    wei0 = np.array(range(1,np.size(seqarray,0)+2))
    def downweigh(x):
        return 1/math.exp((x-1)/tau)
    downweigh_v = np.vectorize(downweigh)
    wei1 = downweigh_v(wei0)
    wei1 = wei1[::-1]
    
    
    #matplotlib.rc('figure', figsize=(7, 5))   # this is to overwrite default aspect of graph to make x-axis longer
    #fig, weiplot = plt.subplots()
    #weiplot.plot(wei0, wei1, 'g', marker='o',  markersize=4)
    #weiplot.set_ylabel('Trial weight', color='g', fontsize=20)
    #weiplot.tick_params('y', colors='g')
    #weiplot.set_xlabel('Trial', fontsize=20)
    #fig.tight_layout()
    #plt.savefig("Weighingfun_tau="+str(tau)+".jpg", dpi=400)
    #plt.clf()
    
    # Fill first row
    row=0
    #print(row)
    baysur_sum = 0  
    prederr_sum = 0
    
    for col in range(0, np.size(seqarray,1)):
        past = seqarray[0:row+1,col]
        past = np.insert(past, 0, alpha0)
        pasttotal = np.ones(row+1)
        pasttotal = np.insert(pasttotal, 0, alpha0+beta0)
        seqarray2[row, -1] = sum(pasttotal*wei1[len(wei1)-row-2:len(wei1)+1])
        alphapost = sum(past*wei1[len(wei1)-row-2:len(wei1)+1])
        betapost = sum((pasttotal-past)*wei1[len(wei1)-row-2:len(wei1)+1])
        seqarray2[row, col] = alphapost
        div = divergence(alphapost, betapost, alpha0, beta0)         
        baysur_sum = baysur_sum + div
    
    seq_input.loc[row+1, 'baysur'] = baysur_sum
    
    
    # Proceed to the other trials/rows, using the posterior alpha and beta from the preceding trial as 
    # new prior alpha and beta
    for row in range(1, np.size(seqarray,0)):
        #print(row)
        baysur_sum = 0  
        prederr_sum = 0
        
        for col in range(0, np.size(seqarray,1)):
            past = seqarray[0:row+1,col]
            past = np.insert(past, 0, alpha0)
            pasttotal = np.ones(row+1)
            pasttotal = np.insert(pasttotal, 0, alpha0+beta0)
            seqarray2[row, -1] = sum(pasttotal*wei1[len(wei1)-row-2:len(wei1)+1])
            alphapost = sum(past*wei1[len(wei1)-row-2:len(wei1)+1])
            betapost = sum((pasttotal-past)*wei1[len(wei1)-row-2:len(wei1)+1])
            seqarray2[row, col] = alphapost
            alphapri = seqarray2[row-1, col]
            betapri = seqarray2[row-1, -1] - seqarray2[row-1, col]
            div = divergence(alphapost, betapost, alphapri, betapri)         
            baysur_sum = baysur_sum + div
        
        seq_input.loc[row+1, 'baysur'] = baysur_sum
        
    output = seq_input.loc[:, 'baysur':'prederr']
    
    return output
    
