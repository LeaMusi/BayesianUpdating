#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea
"""

import os
import time
import pandas as pd
from FirstLevelFit import FirstLevelFit

os.chdir("/Users/ringelblume/Desktop/GitHub/Bayesian_Modeling/")


firstlevel = pd.DataFrame(columns=['subject', 'minutes_elapsed', 'cost_function', 'optimal_tau', 'regr_slope', 'regr_intercept'])

for sub in range(2,6):
    
    starttime = time.time() # Check time
    
    (opttau, costfun, ml_lm) = FirstLevelFit(subj=sub, iters=20, bounds=[5, 1000])
    
    elapsed = time.time() - starttime # Compute time needed for optimization
    
    firstlevel.loc[sub-1,:] = [str(sub), round(elapsed)/60, costfun, opttau, ml_lm.coef_[0], ml_lm.intercept_]
    
    firstlevel.to_csv("firstlevel_parameters_bounds5_1000.csv", sep=";")