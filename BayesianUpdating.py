# -*- coding: utf-8 -*-
# Lea Musiolek, April 2019

"""
Spyder Editor
"""

# Defines a Bayesian updating scheme as a function
# Input arguments:
#   seq_input: A pandas data frame containing feature occurrences (results of Bernoulli processes,
#       with columns representing features/Bernoulli processes and rows representing trials)
#   tau: Parameter determining the steepness of the exponential forgetting mechanism for past trials
#   alpha0: Initial prior alpha value for the Bayesian updating on each feature/Bernoulli process
#   beta0: Initial prior beta value for the Bayesian updating on each feature/Bernoulli process


def BayesianUpdating(seq_input, tau, alpha0, beta0):
    import pandas as pd
    import numpy as np
    import math
    from kl_dirichlet import kl_dirichlet
    
    features = list(seq_input.dtypes.index)[0:len(seq_input.columns)]
    newheads = [s + '_alphapost' for s in features]
    seq_input = pd.concat([seq_input,pd.DataFrame(columns=newheads)], sort=False)
    seq_input['whole'] = np.NaN
    seq_input['baysur'] = np.NaN  
    seq_input['prederr'] = np.NaN
    
    # Compute Bayesian updating for first trial using a prior based on alpha0 and beta0
    const = 1/math.exp((1)/tau)    
    seq_input.loc[1,'whole'] = 1 + 2*const
    baysur_sum = 0  
    prederr_sum = 0
    
    for col in features:
        past = seq_input.loc[0:1,col]
        alphapost = sum(past)+const
        betapost = sum((1-past))+const
        seq_input.loc[1,col+'_alphapost'] = alphapost
        kldiv = kl_dirichlet([alphapost, betapost], [alpha0, beta0])
        baysur_sum = baysur_sum + kldiv # Add up KL divergence across features/Bernoulli processes on this trial
    
    seq_input.loc[1,'baysur'] = baysur_sum
    
    
    # Proceed to the other trials/rows, using the posterior alpha and beta from the preceding trial as 
    # new prior alpha and beta
    for row in range(2, len(seq_input.index)+1):
    
        wei0 = np.array(range(1,row+1))
        def downweigh(x):
            return 1/math.exp((row-x)/tau)
        downweigh_v = np.vectorize(downweigh)
        wei1 = downweigh_v(wei0)
        const = downweigh_v(0)
        seq_input.loc[row,'whole'] = sum(wei1) + 2*const
        baysur_sum = 0  
        prederr_sum = 0
             
        for col in features:
            past = seq_input.loc[0:row,col]
            alphapost = sum(past*wei1)+const
            betapost = sum((1-past)*wei1)+const
            seq_input.loc[row, col+'_alphapost'] = alphapost
            alphapri = seq_input.loc[row-1, col+'_alphapost']
            betapri = seq_input.loc[row-1, 'whole'] - seq_input.loc[row-1, col+'_alphapost']
            kldiv = kl_dirichlet([alphapost, betapost], [alphapri, betapri])         
            baysur_sum = baysur_sum + kldiv
        
        seq_input.loc[row, 'baysur'] = baysur_sum
        
    output = seq_input.loc[:, 'baysur':'prederr']
    return output
    
