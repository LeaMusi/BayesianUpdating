 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %Lea
"""

import os
import time
import pandas as pd
from FirstLevelFit import FirstLevelFit

os.chdir("/Users/ringelblume/Desktop/GitHub/Semantic_Surprise_N400/SemSur_modeling/")
simul = 0


if simul == 1:
    firstlevel = pd.DataFrame(columns=['simufile', 'minutes_elapsed', 'cost_function', 'tau', 'slope_wordreps', 'slope_Typefrequenz_absolut', 'slope_Nachbarn_mittel_absolut', 'slope_Typelaenge_Zeichen', 'slope_baysur', 'regr_intercept', 'sigmasqr'])
elif simul == 0:    
    firstlevel = pd.DataFrame(columns=['subject', 'minutes_elapsed', 'cost_function', 'tau', 'slope_wordreps', 'slope_Typefrequenz_absolut', 'slope_Nachbarn_mittel_absolut', 'slope_Typelaenge_Zeichen', 'slope_baysur', 'regr_intercept', 'sigmasqr'])

for sub in range(1,41): # when simul == 1, sub stands for the counter of simulation files, not for subjects
    
    starttime = time.time() # Check time
    
    (opttau, costfun, ml_lm, sigmasq) = FirstLevelFit(simul=simul, subj=sub)
    
    elapsed = time.time() - starttime # Compute time needed for calculation
    
    firstlevel.loc[sub-1,:] = [str(sub), round(elapsed)/60, costfun, opttau, ml_lm.coef_[0], ml_lm.coef_[1], ml_lm.coef_[2], ml_lm.coef_[3], ml_lm.coef_[-1], ml_lm.intercept_, sigmasq]
    
    if simul == 1:
        firstlevel.to_csv("Simul_parameters.csv", sep=";")
    elif simul == 0:
        firstlevel.to_csv("SemSur_parameters.csv", sep=";")