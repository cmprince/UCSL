'''
Solution to UCSL Python core challenge
Created on Aug 8, 2015

@author: cmp670@nyu.edu
'''

import numpy as np                      #for numpy arrays on which to do the analysis
import datetime as dt                   #for string to time formatting
import matplotlib as mpl                #the graphing utility
from matplotlib import pyplot as pl     #shortcut for the main plotting functions
from mpl_toolkits.axes_grid1 import make_axes_locatable     #see addCBar function for use
import pandas as pd                     #for reading the citi bike data from csv into dataframe

def myLabeledColorBar(axes, bounds, textlabs=[''], colorlist=['gray'], drawedges = True, orientation = 'horizontal'):
    #use color list to create colormap for colorbar
    cmap = mpl.colors.ListedColormap(colorlist)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    
    #create the colorbar with the boundaries passed in bounds
    cb = mpl.colorbar.ColorbarBase(axes, cmap=cmap,
                                         norm=norm,
                                         boundaries=bounds,
                                         drawedges=drawedges,
                                         spacing='proportional',
                                         orientation=orientation)

    #Draw labels along the x-axis if the colorbar is horizontal, otherwise draw them on the y-axis.
    #Draw the labels in the centers of the regions set by the boundaries.
    if (orientation == 'horizontal'):
        cb.ax.get_xaxis().set_ticks([])
        for j in range(len(bounds[1:])):
            cb.ax.text(((bounds[j+1]-bounds[j])/2 + bounds[j])/float(bounds[-1]),
                       .5,
                       textlabs[j % len(textlabs)] + '\n' + '{0:g}'.format((bounds[j+1]-bounds[j])),
                       ha='center', va='center')
                       #bbox=dict(facecolor='white', ec='none', alpha=0.65))

    else:
        cb.ax.get_yaxis().set_ticks([])
        for j in range(len(bounds[1:])):
            cb.ax.text(.5,
                       ((bounds[j+1]-bounds[j])/2 + bounds[j])/float(bounds[-1]),
                       textlabs[j % len(textlabs)] + '\n' + '{0:g}'.format((bounds[j+1]-bounds[j])),
                       ha='center', va='center')
                       #bbox=dict(facecolor='white', ec='none', alpha=0.65))
    
    return cb

def addCBar(im, ax, ticks=5, side='top', size='5%', pad=0.03):
    #create region in ax in which to draw colorbar
    divider = make_axes_locatable(ax)
    caxnew=divider.append_axes(side, size=size, pad=pad)
    
    #Determine colorbar orienation from the side argument
    orientation='horizontal'
    if (side=='left' or side=='right'): orientation='vertical'
    
    #Create the colorbar from data im and set tick locations from the side argument
    cbar=figh.colorbar(im, cax=caxnew, orientation = orientation)
    cbar.ax.tick_params(labeltop=(side=='top'), labelbottom=(side=='bottom'),
                        top=(side=='top'), bottom=(side=='bottom'),
                        labelleft=(side=='left'), labelright=(side=='right'),
                        left=(side=='left'), right=(side=='right'),
                        labelsize='small')

    #Autogenerate good looking ticks for the colorbar
    tick_locator = mpl.ticker.MaxNLocator(nbins=ticks)
    cbar.locator = tick_locator
    cbar.update_ticks()
    return cbar

########
#Read file into a pandas data frame
fname = '../../R/ch2/2014-07 - Citi Bike trip data.csv'
dataperiod = 'July 2014'        #for graph titling (so change this for a different data set)
cbdata=pd.read_csv(fname, parse_dates=['starttime']) #<- nrows for testing purposes

#Subset start days and times by genders and usertypes 
hours = np.zeros(len(cbdata))
days = np.zeros(len(cbdata))
hours = [cbdata['starttime'][h].hour for h in range(len(cbdata))]
days = [cbdata['starttime'][d].day for d in range(len(cbdata))]
menhours = [cbdata['starttime'][h].hour for h in range(len(cbdata)) if cbdata['gender'][h] == 1] 
mendays = [cbdata['starttime'][d].day for d in range(len(cbdata)) if cbdata['gender'][d] == 1]
womenhours = [cbdata['starttime'][h].hour for h in range(len(cbdata)) if cbdata['gender'][h] == 2] 
womendays = [cbdata['starttime'][d].day for d in range(len(cbdata)) if cbdata['gender'][d] == 2]
unknownhours = [cbdata['starttime'][h].hour for h in range(len(cbdata)) if cbdata['gender'][h] == 0]
custhours = [cbdata['starttime'][h].hour for h in range(len(cbdata)) if cbdata['usertype'][h] == 'Customer'] 
custdays = [cbdata['starttime'][d].day for d in range(len(cbdata)) if cbdata['usertype'][d] == 'Customer']
subschours = [cbdata['starttime'][h].hour for h in range(len(cbdata)) if cbdata['usertype'][h] == 'Subscriber'] 
subscdays = [cbdata['starttime'][d].day for d in range(len(cbdata)) if cbdata['usertype'][d] == 'Subscriber']

#Compute histograms for each gender and usertype
numMale, binsm = np.histogram(menhours,range(0,24))
numFemale, binsf = np.histogram(womenhours,range(0,24))
numUnknown, binsu = np.histogram(unknownhours,range(0,24))
numCust, binsc = np.histogram(custhours,range(0,24))
numSubsc, binss = np.histogram(subschours,range(0,24))
           
totalMale = numMale.sum()
totalFemale = numFemale.sum()
totalUnknown = numUnknown.sum()
totalCust = numCust.sum()
totalSubsc = numSubsc.sum()
numTotal = totalMale + totalFemale + totalUnknown   #should be equal to len(cbdata)

#Caluclate the average tripduration (first part of challenge):
avTripduration = cbdata['tripduration'].mean()
print 'Read n=' + str(len(cbdata)) + ' records from data set ' + fname + \
      '. The average tripduration is ' + '{0:.2f}'.format(avTripduration) + ' seconds.'

#Visualization (second part of challenge):
#Setup figure subplot grid:
#=============
#|11111111111|
#|-+---+---+-|
#|6|222|444|7|
#|6+---+---+7|
#|6|333|555|7|
#=============

figh = pl.figure(figsize=(8,10))
ax1 = pl.subplot2grid((3,6), (0,0), colspan=6)
ax2 = pl.subplot2grid((3,6), (1,1), colspan=2)
ax3 = pl.subplot2grid((3,6), (2,1), colspan=2, sharex=ax2, sharey=ax2)
ax4 = pl.subplot2grid((3,6), (1,3), colspan=2, sharex=ax2, sharey=ax2)
ax5 = pl.subplot2grid((3,6), (2,3), colspan=2, sharex=ax2, sharey=ax2)
ax6 = pl.subplot2grid((3,6), (1,0), rowspan=2)
ax7 = pl.subplot2grid((3,6), (1,5), rowspan=2)
#It's a crowded plot, so let's use most of the canvas:
figh.subplots_adjust(top=0.95,bottom=0.05,left=0.1,right=0.95)

#Construct a histogram for the rides by hour
pl.sca(ax1)
bincolors=['lightgray']*4 + ['khaki']*4
c,b,patches=ax1.hist(hours, 24,
                     range=(0,24), align='left',
                     color='gray', label='Total rides')
#Color bins using bincolors ('% len(list)' permits recycling of the list)
for i,patch in enumerate(patches):
    patch.set_facecolor(bincolors[i % len(bincolors)])  
    patch.set_edgecolor('gray')
#Add lines to the plot for each group histogram
l1, = pl.plot(numMale, label='Male', color='deepskyblue', linewidth=3)
l2, = pl.plot(numFemale, label='Female', color='tomato', linewidth=3)
l3, = pl.plot(numUnknown, label='Unknown', color='limegreen', linewidth=3)
l4, = pl.plot(numCust, label='Customers', color='pink', linewidth=3)
l5, = pl.plot(numSubsc, label='Subscribers', color='orange', linewidth=3)
#Add a legend
ax1.legend(loc='upper left', ncol=1, fontsize='small')
#align='left' in the hist call aligns bins to the centers of the ticks,
#so adjust the range to extend a little beyond -0.5 and +23.5
ax1.set_xlim(left=-1,right=24)
ax1.set_xticks([0,4,8,12,16,20,23])
pl.title('Total Citi Bike rides in ' + dataperiod + ' by hour, per gender and usertype')
pl.xlabel('hour of the day', labelpad=0.1)
#manually bump the axis up the figure a bit to avoid label interference
ax1.set_position([.1,.725,.85,.225])

#Create four 2-d histograms binning by hour and day
#Male riders:
pl.sca(ax2)
c2,x,y,mh2 = ax2.hist2d(menhours, mendays, [range(0,25),range(1,33)])
ax2.set_xlim(right=24)
#Add appropriate axis labels where needed
pl.xlabel('hour', labelpad=0.1)
pl.ylabel('day of the month', labelpad=0)
#Add a customized color bar (see function addCBar above)
cbar2=addCBar(mh2,ax2)
ax2.tick_params(left=False, labelleft=False, labelsize='small', pad=0)
#Label the plot
ax2.text(0,1,'men',
         color='white', horizontalalignment='left', verticalalignment='top',
         transform=ax2.transAxes)
#Since all hist2d calls share axes, only need to do this once
ax2.set_xticks([0,4,8,12,16,20,23])
ax2.set_yticks([7,14,21,28])

#Female riders: 
pl.sca(ax3)
c,x,y,wh2 = ax3.hist2d(womenhours, womendays, [range(0,25),range(1,33)])
pl.ylabel('day of the month', labelpad=0)
cbar3=addCBar(wh2,ax3, side='bottom')
ax3.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False, 
                left=False, labelleft=False, labelsize='small', pad=0)
ax3.text(0,1,'women',
         color='white', horizontalalignment='left', verticalalignment='top',
         transform=ax3.transAxes)

#Customers:
pl.sca(ax4)
c,x,y,ch2 = ax4.hist2d(custhours, custdays, [range(0,25),range(1,33)])
ax4.set_xlim(right=24)
pl.xlabel('hour', labelpad=0.05)
cbar4=addCBar(ch2,ax4)
ax4.tick_params(labelsize='small', pad=0)
ax4.text(0,1,'customers',
         color='white', horizontalalignment='left', verticalalignment='top',
         transform=ax4.transAxes)

#Subscribers:
pl.sca(ax5)
c,x,y,sh2 = ax5.hist2d(subschours, subscdays, [range(0,25),range(1,33)])
cbar3=addCBar(sh2,ax5, side='bottom')
ax5.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False, labelsize='small', pad=0)
ax5.text(0,1,'subscribers',
         color='white', horizontalalignment='left', verticalalignment='top',
         transform=ax5.transAxes)

#I dislike pie charts, so here is an alternative I constructed with color bars
#See function myLabeledColorBar above.
collist1 = ['tomato', 'deepskyblue', 'limegreen']
lablist1 = ['Women', 'Men', 'Unknown']
bounds1 = [0, totalFemale, totalMale + totalFemale, numTotal]
cb2 = myLabeledColorBar(ax6, bounds1, lablist1, collist1, orientation='vertical')

collist2 = ['orange', 'pink']
lablist2 = ['Subscribers','Customers']
bounds2 = [0, totalSubsc, totalCust + totalSubsc]
cb3 = myLabeledColorBar(ax7, bounds2, lablist2, collist2, orientation='vertical')

#And finally render the whole plot
pl.show()
