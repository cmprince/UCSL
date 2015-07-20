#
# NYU-CUSP UCSL
# R Challenge no. 2
# Christopher Prince
#

#import Jan 2015 'clean' CitiBike data from csv file, include a header line
fname <- '~/UCSL/R/ch2//Citi Bike Clean Data.csv'
cbdata <- read.csv(fname, header = TRUE)

summary(cbdata)
n <- dim(cbdata)[1]
s <- sd(cbdata$tripduration)
xbar <- mean(cbdata$tripduration)
xmed <- median(cbdata$tripduration)

hist(cbdata$tripduration, breaks = c((1:60)*60,100000), probability = TRUE, xlim=c(0,3600))
xfit <- seq(xbar-4*s,xbar+4*s)
yfit <- dnorm(xfit, mean = xbar, sd = s)
lines(xfit, yfit, lwd=3, col='orange')

# H_0: median(tripduration) = 900
# H_a: median(tripduration) > 900
# Because n=20853, and histogram is not wildly skewed (out-of-normal), CLT applies. 
# Intuitively, subsampled medians seem like they should distrubute normally in the same manner that the mean does.
# Some googling turns up 
# This calls for a upper-tail test of the mean. Since the population variance is not known we will use
# the t-statistic instead of the z-statistic.


med_h0 <- 900   #the hypothesized median
alpha <- 0.05 #significance level

(xmed-med_h0)/(s/sqrt(n))
qt(1-alpha,df=n-1)

#
#Because the median is larger than the mean, and the sample size is so large, we can also infer this using a 'pure'
#t-test of the mean if we cannot reject a hypothesis of the mean being less than or equal to 900:

t.test(cbdata$tripduration, mu=mu, alternative = "greater")
