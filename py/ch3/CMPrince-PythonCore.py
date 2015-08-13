'''
Created on Aug 8, 2015

@author: cmp670
'''

import csv                  #for reading the citi bike data file from csv
import numpy as np          #for numpy arrays on which to do the analysis
import datetime as dt       #for string to time formatting
import matplotlib as mpl
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

def myLabeledColorBar(axes, bounds, textlabs=[''], colorlist=['gray'], drawedges = True, orientation = 'horizontal'):
    cmap = mpl.colors.ListedColormap(colorlist)

    # If a ListedColormap is used, the length of the bounds array must be
    # one greater than the length of the color list.  The bounds must be
    # monotonically increasing.

    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cb = mpl.colorbar.ColorbarBase(axes, cmap=cmap,
                                         norm=norm,
                                         boundaries=bounds,
                                         drawedges=drawedges,
                                         spacing='proportional',
                                         orientation=orientation)

    if (orientation == 'horizontal'):
        cb.ax.get_xaxis().set_ticks([])
        for j in range(len(bounds[1:])):
            cb.ax.text(((bounds[j+1]-bounds[j])/2 + bounds[j])/bounds[-1],
                       .5,
                       textlabs[j % len(textlabs)] + '\n' + '{0:g}'.format((bounds[j+1]-bounds[j])),
                       ha='center', va='center',
                       bbox=dict(facecolor='white', ec='none', alpha=0.65))

    else:
        cb.ax.get_yaxis().set_ticks([])
        for j in range(len(bounds[1:])):
            cb.ax.text(.5,
                       ((bounds[j+1]-bounds[j])/2 + bounds[j])/bounds[-1],
                       textlabs[j % len(textlabs)] + '\n' + '{0:g}'.format((bounds[j+1]-bounds[j])),
                       ha='center', va='center',
                       bbox=dict(facecolor='white', ec='none', alpha=0.65))
    
    return cb

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
menhours = [cbdata['starttime'][h].hour for h in range(len(cbdata)) if cbdata['gender'][h] == 1] 
mendays = [cbdata['starttime'][d].day for d in range(len(cbdata)) if cbdata['gender'][d] == 1]
womenhours = [cbdata['starttime'][h].hour for h in range(len(cbdata)) if cbdata['gender'][h] == 2] 
womendays = [cbdata['starttime'][d].day for d in range(len(cbdata)) if cbdata['gender'][d] == 2]
custhours = [cbdata['starttime'][h].hour for h in range(len(cbdata)) if cbdata['usertype'][h] == 'Customer'] 
custdays = [cbdata['starttime'][d].day for d in range(len(cbdata)) if cbdata['usertype'][d] == 'Customer']
subschours = [cbdata['starttime'][h].hour for h in range(len(cbdata)) if cbdata['usertype'][h] == 'Subscriber'] 
subscdays = [cbdata['starttime'][d].day for d in range(len(cbdata)) if cbdata['usertype'][d] == 'Subscriber']

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
           
print (cbdata['usertype'])
print (numMale, numFemale, numUnknown, numCust, numSubsc)

totalMale = numMale.sum()
totalFemale = numFemale.sum()
totalUnknown = numUnknown.sum()
totalCust = numCust.sum()
totalSubsc = numSubsc.sum()
numTotal = totalMale + totalFemale + totalUnknown

pctMale = totalMale/numTotal
pctFemale = totalFemale/numTotal

figh = pl.figure()
ax1 = pl.subplot2grid((3,6), (0,0), colspan=6)
ax2 = pl.subplot2grid((3,6), (1,0), colspan=2)
ax3 = pl.subplot2grid((3,6), (2,0), colspan=2, sharex=ax2, sharey=ax2)
ax4 = pl.subplot2grid((3,6), (1,2), rowspan=2)
ax5 = pl.subplot2grid((3,6), (1,3), rowspan=2)
ax6 = pl.subplot2grid((3,6), (1,4), colspan=2, sharex=ax2, sharey=ax2)
ax7 = pl.subplot2grid((3,6), (2,4), colspan=2, sharex=ax2, sharey=ax2)

pl.sca(ax1)
ax1.hist(hours, 24, range=(0,24), align='left', color='gray', label='Total rides')
l1, = pl.plot(numMale, label='Male')
l2, = pl.plot(numFemale, label='Female')
l3, = pl.plot(numUnknown, label='Unknown gender')
ax1.legend(loc='upper left')
ax1.set_xlim(left=-1,right=24)

pl.sca(ax2)
c,x,y,mh2 = ax2.hist2d(menhours, mendays, [range(0,25),range(1,33)])
ax2.set_xlim(right=24)
pl.colorbar(mh2)
 
pl.sca(ax3)
c,x,y,wh2 = ax3.hist2d(womenhours, womendays, [range(0,25),range(1,33)])
pl.setp( ax3.get_xticklabels(), visible=False)
pl.colorbar(wh2)

pl.sca(ax6)
c,x,y,ch2 = ax6.hist2d(custhours, custdays, [range(0,25),range(1,33)])
ax6.set_xlim(right=24)
pl.colorbar(ch2)
 
pl.sca(ax7)
c,x,y,sh2 = ax7.hist2d(subschours, subscdays, [range(0,25),range(1,33)])
pl.setp( ax7.get_xticklabels(), visible=False)
pl.colorbar(sh2)

collist1 = ['r', 'g', 'b']
lablist1 = ['Men', 'Women', 'Unknown']
bounds1 = [0, totalMale, totalMale + totalFemale, numTotal]
cb2 = myLabeledColorBar(ax4, bounds1, lablist1, collist1, orientation='vertical')

collist2 = ['yellow', 'pink']
lablist2 = ['Customers', 'Subscribers']
bounds2 = [0, totalCust, totalCust + totalSubsc]
cb3 = myLabeledColorBar(ax5, bounds2, lablist2, collist2, orientation='vertical')

pl.show()

if __name__ == '__main__':
    pass