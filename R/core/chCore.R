#fname <- '~/UCSL/R/ch2/2014-07 - Citi Bike trip data.csv'
fname <- '~/UCSL/R/ch2/Citi Bike Clean Data.csv'   #smaller set for testing
cbd<-read.csv(fname,header=TRUE)

#get tripduration parameters for z-score calcluation
tdur.mean <- mean(cbd$tripduration)
tdur.sd <- sd(cbd$tripduration)
#Create a z-score metric
z_sc <- (cbd$tripduration-tdur.mean)/tdur.sd
#Let's create a naive distance metric (as-the-crow-flies, not distance travelled)
dist <- acos(sin(cbd$start.station.latitude*pi/180)*sin(cbd$end.station.latitude*pi/180)+cos(cbd$start.station.latitude*pi/180)*cos(cbd$end.station.latitude*pi/180)*cos((cbd$start.station.longitude-cbd$end.station.longitude)*pi/180))*6371000
#append these to our data frame
cbd <- cbind(cbd, dist, z_sc)

##no outlier removal
#Data summaries
summary(cbd$tripduration)
summary(cbd$birth.year)
summary(cbd$dist)

#Histograms
par(mfrow = c(3,1))
hist(cbd$tripduration)
hist(cbd$birth.year)
hist(cbd$dist)

#Boxplots
par(mfrow = c(1,3))
boxplot(cbd$tripduration)
boxplot(cbd$birth.year)
boxplot(cbd$dist)

#xy-plots
par(mfrow = c(1,1))
plot(cbd$birth.year, cbd$tripduration)
symbols(cbd$birth.year, cbd$tripduration, circles=array(0,dim(cbd)[1]), xlim=c(1920,2000))
symbols(cbd$birth.year, cbd$tripduration, circles=array(0,dim(cbd)[1]), xlim=c(1920,2000), ylim=c(60,2000))

#intensity plots
makeIntHistBins <- function(x, y, xrng = c(min(x):max(x)), ybrks = 30) {
  td<-array(0,c(length(xrng),length(ybrks)))
  count=0
  for (i in c(min(x):max(x))){
    count<- count + 1
    s<-subset(cbd, birth.year==i)
    t<-hist(s$tripduration, breaks=ybrks, plot=FALSE)
    td[count,]=t$counts
  }
  return(td)
}

td1<-array(0,c(81,74))

count=0
for (i in c(1920:2000)){
  count<- count + 1
  s<-subset(cbd, birth.year==i)
  t<-hist(s$tripduration, breaks=60*c(1:60,15*c(5:12),60*c(4:10)), plot=FALSE)
  td1[count,]=t$counts
}

image(c(1920:2000), 60*c(1:60,15*c(5:12),60*c(4:10)), td1, xlim=c(1920,2000), ylim=c(60,2000), col=rainbow(30))
#image(c(1920:2000), 60*c(1:60,15*c(5:12),60*c(4:10)), td1, xlim=c(1920,2000), ylim=c(60,2000), col=c(gray(100:0/100)))

td2<-array(0,c(81,40))

count=0
for (i in c(1920:2000)){
  count<- count + 1
  s<-subset(cbd, birth.year==i)
  t<-hist(s$dist, breaks=250*c(0:40), plot=FALSE)
  td2[count,]=t$counts
}

image(c(1920:2000), 250*c(1:40), td2, xlim=c(1920,2000), ylim=c(60,6000), col=rainbow(30))
#image(c(1920:2000), 250*c(1:40), td2, xlim=c(1920,2000), ylim=c(60,6000), col=c(gray(100:0/100)))

#Create a regression function to reuse in this document
myregression <- function(x, y){
  x.mean <- mean(x, na.rm = TRUE)
  y.mean <- mean(y, na.rm = TRUE)
  
  #Data frame to calculate regression manually
  data <- data.frame(x, y, xdev=(x-x.mean), ydev=(y-y.mean), xdevydev=((x-x.mean)*(y-y.mean)), xdev2=(x-x.mean)^2,ydev2=(y-y.mean)^2)
  
  #OLS terms
  SP <- sum(data$xdevydev, na.rm=TRUE)
  SSx <- sum(data$xdev2, na.rm=TRUE)
  SSy <- sum(data$ydev2, na.rm=TRUE)
  SSxy <- sum(data$xdevydev, na.rm=TRUE)
  b1 <- SP / SSx
  b0 <- y.mean-b1*x.mean
  
  #Manual calculation of R-squared
  r2 <- SSxy^2/(SSx*SSy)
  
  #get the set names
  xname <- deparse(substitute(x))
  yname <- deparse(substitute(y))
  
  #return the results
  results <- list(b0=b0,b1=b1,r2=r2,xmean=x.mean,ymean=y.mean,xname=xname, yname=yname, x=x,y=y) #, model=model1)
  
  return(results)
}

#plot the regression on an xy plot
myRegPlots <- function(myregr, xlim=c(min(myregr$x, na.rm=TRUE),max(myregr$x, na.rm=TRUE)), ylim=c(min(myregr$y, na.rm=TRUE),max(myregr$y, na.rm=TRUE))){
  plot(myregr$x,myregr$y,col="red", lwd = 1, xlim=xlim, ylim=ylim, xlab=myregr$xname, ylab=myregr$yname, xaxs='i')
  points(myregr$xmean,myregr$ymean,col="green", lwd = 10)
  lines(xlim,myregr$b0+myregr$b1*xlim, lwd=4)  
}

#plot the regression on an intensity plot
myRegPlot2 <- function(myregr, mat, xlim=c(min(myregr$x, na.rm=TRUE),max(myregr$x, na.rm=TRUE)), ylim=c(min(myregr$y, na.rm=TRUE),max(myregr$y, na.rm=TRUE))){
  if (missing(mat)) {
    print ("ERROR: Must provide a matrix to render")
    return(NULL)
  }
  image(xbrks, ybrks, mat, xlim=xlim, col=rainbow(30))
#  plot(myregr$x,myregr$y,col="red", lwd = 1, xlim=xlim, ylim=ylim, xlab=myregr$xname, ylab=myregr$yname)
  points(myregr$xmean,myregr$ymean,col="green", lwd = 10)
  lines(xlim,myregr$b0+myregr$b1*xlim, lwd=4)  
}

##Models
#Start with tripduration as a function of birth year:
modelBYxTDUR<-myregression(x = cbd$birth.year, y = cbd$tripduration)
myRegPlots(myregr = modelBYxTDUR,ylim = c(0,2000))

image(c(1920:2000), 60*c(1:60,15*c(5:12),60*c(4:10)), td1, xlim=c(1920,2000), ylim=c(60,2000), col=rainbow(30))
lines(c(1920:2000),modelBYxTDUR$b0+modelBYxTDUR$b1*c(1920:2000), lwd=3)  
points(modelBYxTDUR$xmean,modelBYxTDUR$ymean,col="black", lwd = 3, bg="white", pch=21)

#Verify using R's lm() method
summary(lm(cbd$tripduration~cbd$birth.year))

#Repeat calculations with our distance metric as a function of birth year:
modelBYxDIST<-myregression(x = cbd$birth.year, y = cbd$dist)
myRegPlots(myregr= modelBYxDIST)
image(c(1920:2000), 250*c(1:40), td2, xlim=c(1920,2000), ylim=c(60,6000), col=rainbow(30))
lines(c(1920:2000),modelBYxDIST$b0+modelBYxDIST$b1*c(1920:2000), lwd=3)  
points(modelBYxDIST$xmean,modelBYxDIST$ymean,col="black", lwd = 3, bg="white", pch=21)
summary(lm(cbd$dist~cbd$birth.year))

#Subset data to remove outliers (z_sc<2)
cbd.z2<-subset(cbd, z_sc<2)

##Outlier removal
#Data summaries
summary(cbd.z2$tripduration)
summary(cbd.z2$birth.year)
summary(cbd.z2$dist)

#Histograms
par(mfrow = c(3,1))
hist(cbd.z2$tripduration)
hist(cbd.z2$birth.year)
hist(cbd.z2$dist)

#Boxplots
par(mfrow = c(1,3))
boxplot(cbd.z2$tripduration)
boxplot(cbd.z2$birth.year)
boxplot(cbd.z2$dist)

#xy-plots
par(mfrow = c(1,1))
plot(cbd.z2$birth.year, cbd.z2$tripduration)
symbols(cbd.z2$birth.year, cbd.z2$tripduration, circles=array(0,dim(cbd.z2)[1]), xlim=c(1920,2000))
symbols(cbd.z2$birth.year, cbd.z2$tripduration, circles=array(0,dim(cbd.z2)[1]), xlim=c(1920,2000), ylim=c(60,2000))

#intensity plots
td3<-array(0,c(81,74))

count=0
for (i in c(1920:2000)){
  count<- count + 1
  s<-subset(cbd.z2, birth.year==i)
  t<-hist(s$tripduration, breaks=60*c(1:60,15*c(5:12),60*c(4:10)), plot=FALSE)
  td3[count,]=t$counts
}

image(c(1920:2000), 60*c(1:60,15*c(5:12),60*c(4:10)), td3, xlim=c(1920,2000), ylim=c(60,2000), col=rainbow(30))
#image(c(1920:2000), 60*c(1:60,15*c(5:12),60*c(4:10)), td3, xlim=c(1920,2000), ylim=c(60,2000), col=c(gray(100:0/100)))

td4<-array(0,c(81,40))

count=0
for (i in c(1920:2000)){
  count<- count + 1
  s<-subset(cbd.z2, birth.year==i)
  t<-hist(s$dist, breaks=250*c(0:40), plot=FALSE)
  td4[count,]=t$counts
}

image(c(1920:2000), 250*c(1:40), td4, xlim=c(1920,2000), ylim=c(60,6000), col=rainbow(30))
#image(c(1920:2000), 250*c(1:40), td4, xlim=c(1920,2000), ylim=c(60,6000), col=c(gray(100:0/100)))

##Models
#Start with tripduration as a function of birth year:
modelBYxTDUR2<-myregression(cbd.z2$birth.year, cbd.z2$tripduration)
myRegPlots(modelBYxTDUR2)
image(c(1920:2000), 60*c(1:60,15*c(5:12),60*c(4:10)), td3, xlim=c(1920,2000), ylim=c(60,2000), col=rainbow(30))
lines(c(1920:2000),modelBYxTDUR2$b0+modelBYxTDUR2$b1*c(1920:2000), lwd=3)  
points(modelBYxTDUR2$xmean,modelBYxTDUR2$ymean,col="black", lwd = 3, bg="white", pch=21)
summary(lm(cbd.z2$tripduration~cbd.z2$birth.year))

#Repeat calculations with our distance metric as a function of birth year:
modelBYxDIST2<-myregression(cbd.z2$birth.year, cbd.z2$dist)
myRegPlots(modelBYxDIST2)
image(c(1920:2000), 250*c(1:40), td4, xlim=c(1920,2000), ylim=c(60,6000), col=rainbow(30))
lines(c(1920:2000),modelBYxDIST2$b0+modelBYxDIST2$b1*c(1920:2000), lwd=3)  
points(modelBYxDIST2$xmean,modelBYxDIST2$ymean,col="black", lwd = 3, bg="white", pch=21)
summary(lm(cbd.z2$dist~cbd.z2$birth.year))