#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea
"""

import os
import time
from FirstLevelFit import FirstLevelFit

os.chdir("/Users/ringelblume/Desktop/GitHub/Bayesian_Modeling/")


for sub in range(1,2):
    
    starttime = time.time() # Check time
    
    (opttau, negloglike, ml_lm) = FirstLevelFit(subj=sub, iters=10, bounds=[5, 40])
    
    elapsed_20iter = time.time() - starttime # Compute time needed for optimization
    
    #firstlevel = np.array([(str(sub)), elapsed_20iter, opttau, negloglike, ml_lm.coeff)],
    #                       ... dtype=[('name', 'U10'), ('age', 'i4'), ('weight', 'f4')])
