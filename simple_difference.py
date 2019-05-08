#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea
"""

def divergence(alpha1, beta1, alpha2, beta2):
    import numpy as np
    from scipy import special, stats, integrate
        
    # Integrated difference between prior and posterior distributions
    
    result = integrate.quad(lambda x: abs(stats.beta.pdf(x, alpha1, beta1)-stats.beta.pdf(x, alpha2, beta2)), 0, 1)
    
    return result[0]