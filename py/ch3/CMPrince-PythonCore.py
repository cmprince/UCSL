'''
Created on Aug 8, 2015

@author: cmp670
'''

import csv                  #for reading the citi bike data file from csv
import numpy as np          #for numpy arrays on which to do the analysis
import datetime as dt       #for string to time formatting
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
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
ax2 = pl.subplot2grid((3,6), (1,1), colspan=2)
ax3 = pl.subplot2grid((3,6), (2,1), colspan=2, sharex=ax2, sharey=ax2)
ax4 = pl.subplot2grid((3,6), (1,0), rowspan=2)
ax5 = pl.subplot2grid((3,6), (1,5), rowspan=2)
ax6 = pl.subplot2grid((3,6), (1,3), colspan=2, sharex=ax2, sharey=ax2)
ax7 = pl.subplot2grid((3,6), (2,3), colspan=2, sharex=ax2, sharey=ax2)

pl.sca(ax1)
ax1.hist(hours, 24, range=(0,24), align='left', color='gray', label='Total rides')
l1, = pl.plot(numMale, label='Male', color='b', linewidth=3)
l2, = pl.plot(numFemale, label='Female', color='r', linewidth=3)
l3, = pl.plot(numUnknown, label='Unknown', color='g', linewidth=3)
l4, = pl.plot(numCust, label='Customers', color='yellow', linewidth=3)
l5, = pl.plot(numSubsc, label='Subscribers', color='pink', linewidth=3)
ax1.legend(loc='upper left', ncol=2)
ax1.set_xlim(left=-1,right=24)
ax1.set_xticks([0,6,12,18,23])
pl.title('Total rides in period by hour, per gender and usertype')
pl.xlabel('hour of the day', labelpad=0.05)
curpos=ax1.get_position()
ax1.set_position([.125,.725,.775,.225]) #[curpos.bounds[0], 0.8, curpos.bounds[2], curpos.bounds[3]])

pl.sca(ax2)
c2,x,y,mh2 = ax2.hist2d(menhours, mendays, [range(0,25),range(1,33)])
ax2.set_xlim(right=24)
pl.setp( ax2.get_yticklabels(), visible=False)
pl.xlabel('hour of the day', labelpad=0.03)
divider2 = make_axes_locatable(ax2)
cax2=divider2.append_axes("top", size='5%', pad=0.03)
cbar1=figh.colorbar(mh2, cax=cax2, orientation = 'horizontal')
cbar1.ax.tick_params(labeltop='on', labelbottom='off', top='on', bottom='off')
ax2.text(0,0.5,'male riders', color='white', rotation='vertical', verticalalignment='bottom')
ax2.set_xticks([0,6,12,18,23])
ax2.set_yticks([7,14,21,28])
 
pl.sca(ax3)
c,x,y,wh2 = ax3.hist2d(womenhours, womendays, [range(0,25),range(1,33)])
pl.setp( ax3.get_xticklabels(), visible=False)
pl.setp( ax3.get_yticklabels(), visible=False)
divider3 = make_axes_locatable(ax3)
cax3=divider3.append_axes("bottom", size='5%', pad=0.03)
cbar2=figh.colorbar(wh2, cax=cax3, orientation = 'horizontal')
ax3.text(0,0.5,'female riders', color='white', rotation='vertical', verticalalignment='bottom')

pl.sca(ax6)
c6,x,y,ch2 = ax6.hist2d(custhours, custdays, [range(0,25),range(1,33)])
ax6.set_xlim(right=24)
pl.ylabel('day of the month', labelpad=0.03)
divider6 = make_axes_locatable(ax6)
cax6=divider6.append_axes("top", size='5%', pad=0.03)
cbar6=figh.colorbar(ch2, cax=cax6, orientation = 'horizontal')
cbar6.ax.tick_params(labeltop='on', labelbottom='off', top='on', bottom='off')
ax6.text(0,0.5,'customers', color='white', rotation='vertical', verticalalignment='bottom')

pl.sca(ax7)
c,x,y,sh2 = ax7.hist2d(subschours, subscdays, [range(0,25),range(1,33)])
pl.setp( ax7.get_xticklabels(), visible=False)
divider7 = make_axes_locatable(ax7)
cax7=divider7.append_axes("bottom", size='5%', pad=0.03)
figh.colorbar(sh2, cax=cax7, orientation = 'horizontal')
ax7.text(0,0.5,'subscribers', color='white', rotation='vertical', verticalalignment='bottom')

collist1 = ['b', 'r', 'g']
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