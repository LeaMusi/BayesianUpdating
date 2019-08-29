#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea Musiolek
"""

import os
os.chdir(os.path.dirname(__file__))
import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns


# Open file for all participants' condition-wise mean amplitudes
condmeans = pd.DataFrame(columns=['subject', 'condition', 'mean_amplitude'])

############### Aggregating condition-wise mean amplitudes and performing t test across participants
#subj=1
for subj in range(1,41):
    # Read in data
    if subj < 10:
        substr = '0' + str(subj)
    else:
        substr = str(subj)         
    sub_path = 'SemSurSequences/SemSurSequence_' + substr + '.csv'
    dat = pd.read_csv(sub_path, encoding = 'unicode_escape', sep=";", index_col=0)
    
    # Reshape data and aggregate, writing into common file for all participants and saving at each iteration
    dat = dat.rename(columns={"standard": "deviant"})
    dat['deviant'] = dat['deviant'].map({222: 1, 223: 1, 224:np.nan, 225:0})
    dat2 = dat.dropna(axis=0, subset=['deviant'], how="any")
    deviantmean = dat2['meanamp_ROI'][dat2['deviant'] == 1].mean()
    standardmean = dat2['meanamp_ROI'][dat2['deviant'] == 0].mean()
    condmeans.loc[(subj*2)-2,:] = [str(subj), 'deviant', deviantmean]
    condmeans.loc[(subj*2)-1,:] = [str(subj), 'standard', standardmean]
    condmeans.to_csv("cond_meanamps.csv", sep=";")
    
a = condmeans['mean_amplitude'][condmeans['condition'] == 'deviant']
b = condmeans['mean_amplitude'][condmeans['condition'] == 'standard']
ttest = scipy.stats.ttest_rel(a, b, axis=0)
ttest = pd.DataFrame(ttest[0:2])
ttest['parameter']=['T', 'p']
ttest.to_csv("ttest.csv", sep=";")
    

################# Plots für eine Beispiel-VP:


# Deviant- und Surprisedaten
x = dat['seg'][0:100]
y1 = dat['baysur'][0:100]
y2 = dat['deviant'][0:100]

matplotlib.rc('figure', figsize=(12, 5))   # this is to overwrite default aspect of graph to make x-axis longer

fig, ax1 = plt.subplots()

# First plot (background)
ax1.bar(x, y2, width=0.5, color='powderblue')
ax1.yaxis.set_label_position("right")
ax1.yaxis.tick_right()
ax1.set_ylabel('Deviants', color='cadetblue')
ax1.set_yticks([])
ax1.yaxis.set_major_formatter(plt.NullFormatter())

# Creating twin axes
ax2 = ax1.twinx()

#Second plot (foreground)
ax2.plot(x, y1, 'g', marker='o',  markersize=4)
ax2.yaxis.set_label_position("left")
ax2.yaxis.tick_left()
ax2.set_ylabel('Semantic Surprise', color='g')
ax2.tick_params('y', colors='g')
# Displaying grid for the Date axis
ax2.grid(True)

fig.tight_layout()

# Saving graph to file
plt.savefig("deviants_SemSur.jpg", dpi=400)