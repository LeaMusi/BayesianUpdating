#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea
"""

#Defines a function which uses a subject's number, loads their EEG data and stimulus sequence and
# optimizes the tau value for their Bayesian Updating iteratively using the bounded Brent-Dekker method, 
# while fitting a simple linear regression at each step

def FirstLevelFit(subj, iters, bounds):
    from scipy import optimize
    from LinearFit import LinearFit
    
    def LinearFitForOpt(tau, subj):
        (costfun, lm) = LinearFit(tau, subj)
        return costfun
    
    opt = optimize.minimize_scalar(fun=LinearFitForOpt, args=(subj), bounds=bounds, method='Bounded', options={'maxiter':iters})
    opttau = opt.x
    
    (costfun, ml_lm) = LinearFit(opttau, subj)
    
    return opttau, costfun, ml_lm