#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea
"""

import os
from FirstLevelFit import FirstLevelFit

os.chdir("/Users/ringelblume/Desktop/GitHub/Bayesian_Modeling/")


FirstLevel = FirstLevelFit(subj=1, init_tau=30, iters=5)

#subj = 1
#init_tau = 50
