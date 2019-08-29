#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea Musiolek
"""

import os
os.chdir(os.path.dirname(__file__))
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob

filenames = sorted(glob.glob('SemSur_parameters*.csv'))


data = pd.read_csv(filenames[0], encoding = 'unicode_escape', sep=";")


for file in filenames[1:len(filenames)]:
    dataread = pd.read_csv(file, encoding = 'unicode_escape', sep=";")
    data = pd.concat([data, dataread], axis=0)
    
data = data.drop(['Unnamed: 0'], axis=1)
data.reset_index(drop=True,inplace=True)

# Plot histogram of optimal tau values
plt.hist(data.values[:, 3], bins=50)  # arguments are passed to np.histogram
plt.xlabel("Tau", fontsize=12)
plt.savefig('tauplot.png', dpi=400)

plt.close()

# Compute mean and median of slope and intercept
slopemedian = np.median(data.slope_baysur)
slopemean = np.mean(data.slope_baysur)
interceptmedian = np.median(data.regr_intercept)
interceptmean = np.mean(data.regr_intercept)

# Plot regression lines for each participant
for row in range(0, len(data)):
    f = lambda x: data.slope_baysur[row]*x + data.regr_intercept[row]
    # x values of line to plot
    x = np.array([0,1])
    # plot fit
    plt.plot(x, f(x), marker='', linewidth=0.3, alpha=0.9)
    
f = lambda x: slopemedian*x + interceptmedian
# x values of line to plot
x = np.array([0,1])
# plot fit
plt.plot(x, f(x), marker='', c="black", linewidth=1, alpha=0.9)
    
plt.xlabel("Semantic Surprise, normalized", fontsize=12)
plt.ylabel("N400 mean amplitude", fontsize=12)
plt.savefig('linearplots.png', dpi=400)
