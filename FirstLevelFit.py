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
        (negloglike, lm) = LinearFit(tau, subj)
        return negloglike
    
    opt = optimize.minimize_scalar(fun=LinearFitForOpt, args=(subj), bounds=bounds, method='Bounded', options={'maxiter':iters})
    opttau = opt.x
    
    (negloglike, ml_lm) = LinearFit(opttau, subj)
    
    return opttau, negloglike, ml_lm
    
    
#python program for golden section search.  This implementation
#does not reuse function evaluations.
#
#def gss(fun, a, b, tol, gr, args):
#    # golden section search to find the minimum of f on [a,b]
#    #f: a strictly unimodal function on [a,b]
#    c = b - (b - a) / gr
#    d = a + (b - a) / gr 
#    while abs(c - d) > tol:
#        if fun(c, args) < fun(d, args):
#            b = d
#        else:
#            a = c
#
#        # we recompute both c and d here to avoid loss of precision which may lead to incorrect results or infinite loop
#        c = b - (b - a) / gr
#        d = a + (b - a) / gr
#
#    return (b + a) / 2
#
#gss(fun=LinearFit, a=5, b=40, tol=1, gr=7, args=subj)