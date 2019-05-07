#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea
"""

import pandas as pd
import numpy as np
import os
import math
from scipy import stats, special, optimize
from LinearFit import LinearFit



os.chdir("/Users/ringelblume/Desktop/GitHub/Bayesian_Modeling/")

subj = 1
alpha0 = 1
beta0 = 1


if subj < 10:
    substr = '0' + str(subj)
else:
    substr = str(subj)
sub_path = '/Users/ringelblume/Desktop/SemSur/Data/basefile_SemSur_' + substr + ".csv"
seq = pd.read_csv(sub_path, encoding = 'unicode_escape', sep=" ")


optim = optimize.minimize(fun = LinearFit, x0 = 18, args = (seq), method='Nelder-Mead', options={'maxiter': 8})
#LinearFit = LinearFit(tau, seq)
