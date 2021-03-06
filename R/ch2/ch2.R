#
# NYU-CUSP UCSL
# R Challenge no. 2
# Christopher Prince
#

#import Jan 2015 'clean' CitiBike data from csv file, include a header line
fname <- '~/UCSL/R/ch2//Citi Bike Clean Data.csv'
cbdata <- read.csv(fname, header = TRUE)

#Print the summary data and then try to fit a normal distribution to it.
summary(cbdata)
n <- dim(cbdata)[1]
s <- sd(cbdata$tripduration)
xbar <- mean(cbdata$tripduration)
xmed <- median(cbdata$tripduration)

#Overlay a normal distribution curve onto the histogram of the data
hist(cbdata$tripduration, breaks = c((1:60)*60,Inf), probability = TRUE, xlim=c(0,3600))
xfit <- seq(xbar-4*s,xbar+4*s)
yfit <- dnorm(xfit, mean = xbar, sd = s)
lines(xfit, yfit, lwd=3, col='orange')

# The appropriate null and alternative hypotheses are:
# H_0: median(tripduration) <= 900
# H_a: median(tripduration) > 900

# Before we even do any analysis, we note that the null hypothesis is heavily favored in this sampling, since 68.2% of
# values are less than 900. It would be remarkable for a sample of over 20,000 observations be so off-balance from a
# true median over 900. Nevertheless, we perform the calculations to support this.

# Because n=20853, and the histogram is not wildly skewed (out-of-normal), CLT applies. But how do we account for
# the fact that the the t-test hypotheses are not on means? CLT tells us that means of a sufficiently large number of
# samples from a population of any distribution will themselves distribute normally. Does this apply to medians as well?
# Intuitively, subsampled medians seem like they should distrubute normally in the same manner that the mean does.
# Let's run an experiment. First, the histogram suggests that this may follow something like a log-normal distribution.
# The histogram of the log of the times looks like so:
hist(log(cbdata$tripduration), breaks=30, probability = TRUE)

# Looks promising! Let's model a normal distribution on top of this to be sure:
xbarlog<-mean(log(cbdata$tripduration))
slog<- sd(log(cbdata$tripduration))
xfitlog<-seq(xbarlog-4*slog,xbarlog+4*slog, length.out = 50)
yfitlog<-dnorm(xfitlog,mean=xbarlog,sd=slog)
lines(xfitlog,yfitlog,lwd=3,col='green')
# Excellent. Now, we will run an experiment by creating samples of the lognormal distribution and recording their medians:

med<-array()
for(i in 1:10000){
  m<-rlnorm(n=500)
  med[i]<-median(m)
}

# Plotting the histogram and overlaying a normal fit:
hist(med, breaks=30, probability = TRUE)
medmean<-mean(med)
meds<-sd(med)
xfitmed<-seq(medmean-4*meds,medmean+4*meds, length.out = 50)
yfitmed<-dnorm(xfitmed, mean=medmean, sd=meds)
lines(xfitmed, yfitmed, lwd=3, col='blue')

# Based on this analysis, the sample median distribution is normal, so we can be confident using a t-test for the median.
# Since the population variance is not known we will use the t-statistic instead of the z-statistic.
# We calualate the t-statistic and we will reject the null hypothesis if it is greater than the critical value.

med_h0 <- 900   #the hypothesized median
alpha <- 0.05 #significance level

t1<-(xmed-med_h0)/(s/sqrt(n))
qt(1-alpha,df=n-1)
#Or, the p-value:
pt(t1,df = n-1)

# Because the t-statistic is not greater than the critical value, we do not reject the null hypothesis.

###############
#Problem 2
###############

#Subset the overtime data:
cbd_ot<-subset(cbdata, tripduration>2700)
med_ot<-median(cbd_ot$tripduration)

# H_0: median(OT tripduration) = 7200
# H_a: median(OT tripduration) != 7200
# Since the null hypothesis tests for an equality, we need a two-tailed t-test.

med_ot_h0 <- 7200
alpha <- 0.05
s_ot <- sd(cbd_ot$tripduration)
n_ot <- dim(cbd_ot)[1]
  
t2 <- (med_ot-med_ot_h0)/(s_ot/sqrt(n_ot))
qt(1-alpha/2,df=n_ot-1)

# Since the t-statistic is less than the negative critical value, we reject the null hypothesis that the median 
# for overtime is 2 hours.

###############
#Problem 3
###############

#H_0: no difference in OT mean by gender
#H_a: difference in OT mean by gender

anova <- aov(tripduration ~ gender, data = cbd_ot)
summary(anova)
#The critical value for the test is:
qf(1-alpha,1,214)
#Since the F statistic is not greater than the critical value, we do not reject the null hypothesis