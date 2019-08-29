# Approximates the tau parameter of an exponential forgetting function 
# based on data from Woltz 1990, Table 2, synonym repetitions

cat("\014") # Konsole bereinigen
rm(list = ls())

library(ggplot2)
library(readxl)
dataf <- read_excel("~/Desktop/GitHub/Semantic_Surprise_N400/SemSur_modeling/Woltz1990_Table2.xlsx")

# Set basic function
expFunc <- function(x,tau){1/exp((x-1)/tau)}

# Fit hyperbolic function parameters
y <- dataf$LS_rescaled
x <- dataf$Trial_lag
expFuncFitted <- nls(y ~ expFunc(x, tau), start=list(tau=10), control=list(maxiter=200))

coef(expFuncFitted)["tau"]

expFunc <- function(x){1/exp((x-1)/coef(expFuncFitted)["tau"])}
ggplot(data=dataf, aes(x = Trial_lag, y = LS_rescaled))  +
  geom_point(size = 0.5) +
  stat_function(fun = expFunc, colour = "green" , size = 0.5) +
  theme_minimal() + theme(axis.text=element_text(size=14), axis.title=element_text(size=18)) +
  labs(x = "Trial lag", y = "RT savings (opposite of forgetting)")