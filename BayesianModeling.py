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
from scipy import stats, special
from FirstLevelFit import FirstLevelFit


os.chdir("/Users/ringelblume/Desktop/SemSur/Bayesian_Modeling/")

subj = 1
tau = 18
alpha0 = 1
beta0 = 1


if subj < 10:
    substr = '0' + str(subj)
else:
    substr = str(subj)
sub_path = '/Users/ringelblume/Desktop/SemSur/Data/basefile_SemSur_' + substr + ".csv"
seq = pd.read_csv(sub_path, encoding = 'unicode_escape', sep=" ")

#FirstLevelFit(seq, alpha0, beta0)
