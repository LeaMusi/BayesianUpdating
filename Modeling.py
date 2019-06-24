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


firstlevel = pd.DataFrame(columns=['subject', 'minutes_elapsed', 'cost_function', 'optimal_tau', 'baysur_slope', 'regr_intercept', 'sigmasqr'])

for sub in range(1,3): # when simul == 1, sub stands for the counter of simulation files, not for subjects
    
    starttime = time.time() # Check time
    
    (opttau, costfun, ml_lm) = FirstLevelFit(simul=1, subj=sub, iters=30, bounds=[5, 5000], initial_simplex=[[5],[5000]])
    
    elapsed = time.time() - starttime # Compute time needed for optimization
    
    firstlevel.loc[sub-1,:] = [str(sub), round(elapsed)/60, costfun, opttau, ml_lm.coef_[-1], ml_lm.intercept_, '']
    
    firstlevel.to_csv("simul_parameters_bounds5_5000.csv", sep=";")