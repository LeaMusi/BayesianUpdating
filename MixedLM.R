cat("\014") # Konsole bereinigen
rm(list = ls())
library(ggplot2)
library(plot3D)
library(lme4)
# Regressor-Dateien einlesen

setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
data <- read.csv("SemSurSequences/SemSurSequence_01.csv", row.names=1, sep=";")
data$sub <- "01"

for (sub in 2:40){
  if (sub < 10){
    substr <- paste("0", sub, sep="")
  } else {
    substr <- sub
  }
  datanext <- read.csv(paste("SemSurSequences/SemSurSequence_", substr, ".csv", sep=""), row.names=1, sep=";")
  datanext$sub <- substr
  data <- rbind(data, datanext)
}


#controlvars <- c("wordreps", "Typefrequenz_absolut", "Nachbarn_mittel_absolut", "Typelaenge_Zeichen", "baysur")

# Stimulus-ID zu Faktor konvertieren (nötig für verschiedene Zwecke)
data$sub <- as.factor(data$sub)
data$word.y <- as.factor(data$word.y)

modelcomp <- data.frame(matrix(ncol=6, nrow=1))
names(modelcomp) <- c("predictor", "beta", "SE", "Chisq", "df", "pval")

data_use <- data
# Nur die ersten paar Hundert Trials benutzen
#data_use <- subset(data, seg<=1000)

baysur.corr     = lmer(meanamp_ROI ~ wordreps + baysur + (1 | sub) + (1 | word.y), data=data_use, REML=FALSE)
baysur.corr0    = lmer(meanamp_ROI ~ wordreps +          (1 | sub) + (1 | word.y), data=data_use, REML=FALSE)
summary(baysur.corr)
summary(baysur.corr0)
baysur.corraov <- anova(baysur.corr, baysur.corr0, test="Chisq")
modelcomp$predictor <- 'baysur'
sum <- summary(baysur.corr)
modelcomp$beta <- sum$coefficients['baysur', 'Estimate']
modelcomp$SE <- sum$coefficients['baysur', 'Std. Error']
modelcomp$Chisq <- baysur.corraov$Chisq[2]
modelcomp$df <- baysur.corraov$`Chi Df`[2]
modelcomp$pval <- baysur.corraov$`Pr(>Chisq)`[2]
#ggplot(data_use,aes(y = meanamp_ROI, x = baysur)) + geom_point() + geom_smooth(method = 'lm')

write.table(modelcomp, file="lmms_uncorr.csv", sep=";", row.names = FALSE)



