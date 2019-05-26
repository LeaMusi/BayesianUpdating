#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea
"""

#Defines a function which uses a subject's number, loads their EEG data and stimulus sequence and
# optimizes the tau value for their Bayesian Updating iteratively using the Nelder-Mead method, 
# while fitting a simple linear regression at each step

#def FirstLevelFit(subj, iters):
subj=1
iters=20
from scipy import optimize
from LinearFit import LinearFit

result = optimize.minimize_scalar(fun=LinearFit, args=(subj), bounds=[5,40], method='Golden')
    
    #return result