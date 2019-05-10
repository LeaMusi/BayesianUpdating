#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea
"""

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import random

from kl_dirichlet import divergence
#from kl_dirichlet_alt import divergence
#from simple_difference import divergence


alpha0 = 4
alpha1 = 6
total0 = 10
total1 = 11



def KL_plot(alpha0, alpha1, total0, total1):
    beta0 = total0-alpha0
    beta1 = total1-alpha1
    
    div = divergence(alpha1, beta1, alpha0, beta0)  
    
    return div


fig = plt.figure()
ax = plt.axes(projection='3d')

x = np.random.rand(400, 1)*100
y = np.random.rand(len(x), 1)*100 + 2
z = KL_plot(x, y, 121, 122)

ax.scatter(x, y, z)
