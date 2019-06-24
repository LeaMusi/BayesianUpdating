#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea
"""

#Defines a function which uses a subject's number, loads their EEG data and stimulus sequence and
# optimizes the tau value for their Bayesian Updating iteratively using the bounded Brent-Dekker method, 
# while fitting a simple linear regression at each step

def FirstLevelFit(subj, iters, bounds, initial_simplex, simul):
    from scipy import optimize
    from LinearFit import LinearFit
    
    def LinearFitForOpt(tau, subj, simul):
        (costfun, lm) = LinearFit(tau, subj, simul)
        return costfun
    
    def callbackF(x):
        print(x)
    
    opt = optimize.minimize_scalar(fun=LinearFitForOpt, args=(subj, simul), bounds=bounds, method='Bounded', options={'maxiter':iters})
    #opt = optimize.minimize(fun=LinearFitForOpt, x0=1000, args=(subj, simul), method='Nelder-Mead', options={'maxiter':iters, 'initial_simplex':[[5],[5000]]}, callback=callbackF)
    #opt = optimize.basinhopping(func=LinearFitForOpt, x0=1000, full_output=True, minimizer_kwargs={'args':subj, simul}, niter=10, disp=True)
    opttau = opt.x
    
    (costfun, ml_lm) = LinearFit(opttau, subj, simul)
    
    return opttau, costfun, ml_lm