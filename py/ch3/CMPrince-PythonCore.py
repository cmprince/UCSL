'''
Created on Aug 8, 2015

@author: cmp670
'''

import csv                  #for reading the citi bike data file from csv
import numpy as np          #for numpy arrays on which to do the analysis
import datetime as dt       #for string to time formatting
from matplotlib import pyplot as pl

def getCBData(fname, cols=[], dtypes = [np.object0]):
    #Returns a numpy.array containing numpy.dtype formatted data for the fields in list cols from file fname.
    #TODO: figure out what to do when cols, dtypes not provided
    
    #Load csv into list 
    row=[]
    try:
        with open(fname, 'rU') as f:
            rd = csv.DictReader(f)
            for i in rd:
                row.append(i)
    except IOError as e:
        print('Could not open the file ' + fname + '!')
        
    dim2 = len(row)
    
    for (c,d) in zip(cols, dtypes):
        if d == dt.datetime:
            for i in range(dim2):
                row[i][c] = dt.datetime.strptime(row[i][c], '%m/%d/%y %H:%M')  # naive datetime instance

    #initialize the return array with zeros using the types defined in dtypes
    typearray = zip(cols, dtypes)
    data=np.zeros(dim2, typearray)

    #Load the necessary columns into data numpy.array
    try:
        for c in cols:
            data[c]=np.array([row[i][c] for i in range(len(row))])
    except KeyError:
        print('No ' + c + ' key in the .csv file!')
        raise
    
    return data

########
#Define fname, columns and dtypes for the problem and call our function
#fname = '../ch2/dec-2week-2014.csv'
fname = '../../R/ch2/Citi Bike Clean Data.csv'              #file with fewer data points for testing
cols = ['gender','usertype','tripduration','starttime']
dtypes = [np.int8, (np.str_,10), np.int16, dt.datetime] #'datetime64[s]']

cbdata = getCBData(fname, cols, dtypes)

#Sum for each gender type, get the total, and calculate percentages
hours = np.zeros(len(cbdata))
days = np.zeros(len(cbdata))
hours = [cbdata['starttime'][h].hour for h in range(len(cbdata))]
days = [cbdata['starttime'][d].day for d in range(len(cbdata))]

print cbdata['starttime'][1].hour

numMale, numFemale, numUnknown, numCust, numSubsc = np.zeros(24),np.zeros(24),np.zeros(24),np.zeros(24),np.zeros(24)
for i in range(len(cbdata)):
    sh = cbdata['starttime'][i].hour
    if cbdata['gender'][i]==1:
        numMale[sh] += 1
    elif cbdata['gender'][i] == 2:
        numFemale[sh] += 1
    elif cbdata['gender'][i] == 0:
        numUnknown[sh] += 1
    
    if cbdata['usertype'][i] == 'Customer':
        numCust[sh] += 1
    elif cbdata['usertype'][i] == 'Subscriber':
        numSubsc[sh] += 1
           
print cbdata['usertype']
print numMale, numFemale, numUnknown, numCust, numSubsc

totalMale = numMale.sum()
totalFemale = numFemale.sum()
totalUnknown = numUnknown.sum()
numTotal = totalMale + totalFemale + totalUnknown

pctMale = totalMale/numTotal
pctFemale = totalFemale/numTotal

histhour=np.histogram(hours, range(24)) #, range, normed, weights, density)
print histhour
histday = np.histogram(days, range(1,32)) #, range, normed, weights, density)
print histday

figh = pl.figure()
axh = figh.add_subplot(111)
axh.hist(hours, 24, range=(0,24))
axh.set_xlim(right=24)
pl.show()

figh2 = pl.figure()
axh2 = figh2.add_subplot(111)
axh2.hist2d(hours, days, [range(0,25),range(1,33)])
axh2.set_xlim(right=24)
pl.show()

if __name__ == '__main__':
    pass