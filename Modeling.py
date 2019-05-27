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


firstlevel = pd.DataFrame(columns=['subject', 'minutes_elapsed', 'negative_log_likelihood', 'optimal_tau', 'regr_slope', 'regr_intercept'])

for sub in range(1,41):
    
    starttime = time.time() # Check time
    
    (opttau, negloglike, ml_lm) = FirstLevelFit(subj=sub, iters=15, bounds=[5, 40])
    
    elapsed = time.time() - starttime # Compute time needed for optimization
    
    firstlevel.loc[sub-1,:] = [str(sub), round(elapsed)/60, negloglike, opttau, ml_lm.coef_[0], ml_lm.intercept_]
    
    firstlevel.to_csv("firstlevel_parameters.csv", sep=";")