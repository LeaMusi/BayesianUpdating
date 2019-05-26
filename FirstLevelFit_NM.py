#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea
"""

#Defines a function which uses a subject's number, loads their EEG data and stimulus sequence and
# optimizes the tau value for their Bayesian Updating iteratively using the Nelder-Mead method, 
# while fitting a simple linear regression at each step

def FirstLevelFit(subj, init_tau, iters):
    import pandas as pd
    from scipy import optimize
    from LinearFit import LinearFit

    if subj < 10:
        substr = '0' + str(subj)
    else:
        substr = str(subj)
    sub_path = '/Users/ringelblume/Desktop/SemSur/Data/basefile_SemSur_' + substr + ".csv"
    seq = pd.read_csv(sub_path, encoding = 'unicode_escape', sep=" ")
    
    result = optimize.minimize(fun=LinearFit, x0=init_tau, args=(seq), method='Nelder-Mead', options={'maxiter': iters})
    # IMPORTANT!!!! Nelder-Mead method does not take bounds

    
    return result