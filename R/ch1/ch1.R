#'''
#NYU-CUSP UCSL
#R Challenge no. 1
#Christopher Prince
#'''

#import Jan 2015 CitiBike data from csv file, include a header line
fname <- '~/UCSL/R/ch1/201501-citibike-tripdata.csv'
cbdata <- read.csv(fname, header = TRUE)

#calculate descriptive stats and save in variables
#tdur is shorthand for tripduration
cbdata.count <- dim(cbdata)[1]  #1st element of dim() vector is the number of observations

tdur.mean <- mean(cbdata$tripduration)
tdur.var <- var(cbdata$tripduration)
tdur.sd <- sd(cbdata$tripduration)

tdur.min <- min(cbdata$tripduration)
tdur.max <- max(cbdata$tripduration)
tdur.median <- median(cbdata$tripduration)
tdur.qtile <- quantile(cbdata$tripduration)

#COMPUTING Z-SCORE [from JCB code]
z_sc <- (cbdata$tripduration-tdur.mean)/tdur.sd

#creating subsets of data by z_sc
bikedata.z3 <- subset(cbdata, z_sc<3)

# Computing same calculation for data without outliers
dim(cbdata)
summary(cbdata$tripduration)
sd(cbdata$tripduration)

dim(bikedata.z3)
summary(bikedata.z3$tripduration)
sd(bikedata.z3$tripduration)

#histograms of tdur and log(tdur) for all data points and the z_sc<3 subset
par(mfrow=c(2,2))
hist(cbdata$tripduration, main = "Trip Duration", xlab = "time (sec)", col='red')
hist(log(cbdata$tripduration), main = "log(Trip Duration)", xlab = "log(time (sec)", col='red')
hist(bikedata.z3$tripduration, main = "Trip Duration, z_sc<3", xlab = "time (sec)", col='red')
hist(log(bikedata.z3$tripduration), main = "log(Trip Duration, z_sx<3)", xlab = "log(time (sec))", col='red')

#create subsets by usertype
bikedata.subs <- subset(cbdata, cbdata$usertype=='Subscriber')
bikedata.cust <- subset(cbdata, cbdata$usertype=='Customer')
bikedata.z3.subs <- subset(bikedata.z3, bikedata.z3$usertype=='Subscriber')
bikedata.z3.cust <- subset(bikedata.z3, bikedata.z3$usertype=='Customer')

#count the elements of the subsets
bikedata.cust.count <- dim(bikedata.cust)[1]
bikedata.subs.count <- dim(bikedata.subs)[1]
bikedata.z3.cust.count <- dim(bikedata.z3.cust)[1]
bikedata.z3.subs.count <- dim(bikedata.z3.subs)[1]


#verify that the subsets capture all data (i.e., check for blank or mislabeled usertype)
test_msg <- 'Counts match!'    #assume success
if (bikedata.cust.count + bikedata.subs.count !=cbdata.count) {test_msg <- 'Counts do not match!'} #change msg if !=
test_msg
#test comment for git
#histograms of tdur by usertype for z_sc<3 subsets
par(mfrow=c(2,2))
hist(bikedata.z3.subs$tripduration, main = "Subscriber Trip Duration", xlab = "time (sec)", col='red')
hist(log(bikedata.z3.subs$tripduration), main = "log(Subscriber Trip Duration)", xlab = "log(time (sec))", col='red')
hist(bikedata.z3.cust$tripduration, main = "Customer Trip Duration", xlab = "time (sec)", col='red')
hist(log(bikedata.z3.cust$tripduration), main = "log(Customer Trip Duration)", xlab = "log(time (sec))", col='red')

#and boxplots of same
boxplot(bikedata.z3.subs$tripduration, main='Boxplot of subscriber Trip Duration', xlab='time(sec)')
boxplot(log(bikedata.z3.subs$tripduration), main='Boxplot of subscriber Trip Duration', xlab='log(time(sec))')
boxplot(bikedata.z3.cust$tripduration, main='Boxplot of subscriber Trip Duration', xlab='time(sec)')
boxplot(log(bikedata.z3.cust$tripduration), main='Boxplot of subscriber Trip Duration', xlab='log(time(sec))')