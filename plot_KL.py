#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea
"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from kl_dirichlet import divergence
#from kl_dirichlet_alt import divergence
#from simple_difference import divergence


sample = 100


def KL_plot(alpha0, alpha1, total0, total1):
    beta0 = total0-alpha0
    beta1 = total1-alpha1
    
    div = divergence(alpha1, beta1, alpha0, beta0)  
    
    return div

# Random scatter plot
fig = plt.figure()
ax = plt.axes(projection='3d')

x = np.random.rand(sample, 1) * sample
y = np.random.rand(len(x), 1) * sample + 1
z = KL_plot(x, y, sample, sample)

ax.scatter(x, y, z)

# Wireframe plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

X = np.repeat(np.linspace(2,sample+1, sample).reshape(sample,1), sample, axis=1)
Y = np.repeat(np.linspace(1, sample, sample).reshape(1,sample), sample, axis=0)
Z = KL_plot(X, Y, sample, sample)

# Plot a basic wireframe.
ax.plot_wireframe(X, Y, Z, rstride=2, cstride=2)

plt.show()