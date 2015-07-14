#
# NYU-CUSP UCSL
# R Challenge no. 1
# Christopher Prince
#

#import Jan 2015 CitiBike data from csv file, include a header line
fname <- '~/UCSL/R/ch2/2014-07 - Citi Bike trip data.csv'
cbdata <- read.csv(fname, header = TRUE)

summary(cbdata)
tdur.mean = mean(cbdata$tripduration)
tdur.sd = sd(cbdata$tripduration)
z_sc <- (cbdata$tripduration-tdur.mean)/tdur.sd

#creating subset of data for z_sc<3
bikedata.z3 <- subset(cbdata, z_sc<3)
