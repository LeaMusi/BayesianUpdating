 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea
"""

import os
os.chdir("/Users/ringelblume/Desktop/GitHub/Semantic_Surprise_N400/SemSur_modeling/")
import time
import pandas as pd
import numpy as np
from FirstLevelFit import FirstLevelFit


simul = 0

firstlevel = pd.DataFrame(columns=['subject', 'minutes_elapsed', 'cost_function', 'tau', 'slope_wordreps', 'slope_Typefrequenz_absolut', 'slope_Nachbarn_mittel_absolut', 'slope_Typelaenge_Zeichen', 'slope_baysur', 'regr_intercept', 'baysur_pval', 'resid_var'])

for sub in range(1,41): # when simul == 1, sub stands for the counter of simulation files, not for subjects
    
    starttime = time.time() # Check time
    
    (opttau, ols_lm) = FirstLevelFit(simul=simul, subj=sub)
    
    elapsed = time.time() - starttime # Compute time needed for calculation
    
    firstlevel.loc[sub-1,:] = [str(sub), round(elapsed)/60, ols_lm.ssr, opttau, ols_lm.params.wordreps, ols_lm.params.Typefrequenz_absolut, ols_lm.params.Nachbarn_mittel_absolut, ols_lm.params.Typelaenge_Zeichen, ols_lm.params.baysur, ols_lm.params.Intercept, ols_lm.pvalues.baysur, np.var(ols_lm.resid)]

    firstlevel.to_csv("SemSur_parameters.csv", sep=";")
    
# Compute mean and median of slope and intercept
slopemedian = np.median(firstlevel.slope_baysur)
slopemean = np.mean(firstlevel.slope_baysur)
interceptmedian = np.median(firstlevel.regr_intercept)
interceptmean = np.mean(firstlevel.regr_intercept)

with open("firstlevelresults.txt", "w") as text_file:
    text_file.write("Median intercept: " + str(interceptmedian)
    + "\nMedian slope: " + str(slopemedian)
    + "\nMean intercept: " + str(interceptmean)
    + "\nMean slope: " + str(slopemean))
    
    
