#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea
"""

#Defines a function which uses a subject's number, loads their EEG data and stimulus sequence and
# optimizes the tau value for their Bayesian Updating iteratively using the bounded Brent-Dekker method, 
# while fitting a simple linear regression at each step


def FirstLevelFit(subj, simul):
    from LinearFit import LinearFit
    
    ####### Fitting tau
    #from scipy import optimize
    #def LinearFitForOpt(tau, subj, simul):
    #    (costfun, lm, sigmasq) = LinearFit(tau, subj, simul)
    #    return costfun
    #
    #def callbackF(x):
    #    print(x)
    
    #opt = optimize.minimize_scalar(fun=LinearFitForOpt, args=(subj, simul), bounds=bounds, method='Bounded', options={'maxiter':iters})
    #opt = optimize.minimize(fun=LinearFitForOpt, x0=1000, args=(subj, simul), method='Nelder-Mead', options={'maxiter':iters, 'initial_simplex':[[5],[5000]]}, callback=callbackF)
    #opt = optimize.basinhopping(func=LinearFitForOpt, x0=1000, full_output=True, minimizer_kwargs={'args':subj, simul}, niter=10, disp=True)
    #opttau = opt.x
    
    
    
    ####### Using predefined tau based on forgetting data from Woltz 1990
    opttau = 19.84
    ols_lm = LinearFit(opttau, subj, simul, final=1)
    
    return opttau, ols_lm
