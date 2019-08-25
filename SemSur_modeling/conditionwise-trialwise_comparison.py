#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea Musiolek
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

os.chdir("/Users/ringelblume/Desktop/GitHub/Semantic_Surprise_N400/SemSur_modeling/")

subj=1

#for subj in range(1,41):

if subj < 10:
    substr = '0' + str(subj)
else:
    substr = str(subj)        

sub_path = 'SemSurSequences/SemSurSequence_' + substr + '_tau=6.65.csv'
dat = pd.read_csv(sub_path, encoding = 'unicode_escape', sep=";", index_col=0)

dat = dat.rename(columns={"standard": "deviant"})
dat['deviant'] = dat['deviant'].map({222: 1, 223: 1, 224:np.nan, 225:0})


dat2 = dat.dropna(axis=0, subset=["deviant"], how="any")









################# Plots:
sns.boxplot(x='deviant',y='baysur',data=dat)


# Deviant- und Surprisedaten
x = dat['seg'][0:100]
y1 = dat['baysur'][0:100]
y2 = dat['deviant'][0:100]

matplotlib.rc('figure', figsize=(12, 5))   # this is to overwrite default aspect of graph to make x-axis longer

fig, ax1 = plt.subplots()

# First plot (background)
ax1.bar(x, y2, width=0.5, color='powderblue')
ax1.set_ylabel('Deviants', color='cadetblue')
ax1.set_yticks([])
ax1.yaxis.set_major_formatter(plt.NullFormatter())

# Creating twin axes
ax2 = ax1.twiny()
ax3 = ax2.twinx()
ax2.set_xticks([])               # to hide ticks on the second X-axis - top of the graph

#Second plot (foreground)
ax3.plot(x, y1, 'g', marker='o',  markersize=4)
ax3.set_ylabel('Semantic Surprise', color='g')
ax3.tick_params('y', colors='g')
# Displaying grid for the Date axis
ax3.grid(True)

fig.tight_layout()
# Saving graph to file
#plt.savefig(filename + '_annual.png',dpi=300,transparent=True)