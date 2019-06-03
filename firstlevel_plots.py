#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea Musiolek
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob

filenames = sorted(glob.glob('firstlevel_parameters_bounds5_1000*.csv'))


data = pd.read_csv(filenames[0], encoding = 'unicode_escape', sep=";")


for file in filenames[1:len(filenames)]:
    dataread = pd.read_csv(file, encoding = 'unicode_escape', sep=";")
    data = pd.concat([data, dataread], axis=0)
    
data = data.drop(['Unnamed: 0'], axis=1)

plt.hist(data.values[:, 3], bins=50)  # arguments are passed to np.histogram
plt.xlabel("Tau", fontsize=12)
plt.savefig('tauplot.png', dpi=400)


