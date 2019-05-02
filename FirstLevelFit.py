#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea
"""

# 

def FirstLevelFit(seq, alpha0, beta0):
    from BayesianUpdating import BayesianUpdating
    
    input_sequences = seq.drop(['seg', 'badseg', 'meanamp_ROI', 'word.y'], axis=1)

    BayUpdMeasures = BayesianUpdating(input_sequences, tau, alpha0, beta0)
    
    return BayUpdMeasures