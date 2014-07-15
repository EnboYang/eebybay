# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Project:BB Analysis of BATSE GRB

# <markdowncell>

# This script is used to do Bayesian Block analysis with the ascii file of BATSE GRB
# 
# Author:Enbo Yang(enboyang1990@gmail.com)
# 
# Lisence:GPLv2

# <headingcell level=2>

# Module preparing

# <codecell>

import numpy as np
import matplotlib.pyplot as plt
from astroML.plotting import hist as bbhist

# <headingcell level=2>

# Get the Trigger Num

# <codecell>

trig=raw_input('Please input the tigger:')

# <headingcell level=2>

# Create file to save the channel data

# <codecell>

chnum=1
while chnum<=4:
    f=open("%s.time.CH%s"%(trig,chnum),'w')
    f.close()
    chnum+=1

# <headingcell level=2>

# Split data of each channel

# <codecell>

#This part is used to split channel data of the ascii file of a burst
'''
    Because of the bug in numpy.genfromtxt( cannot read a file with differential rows to a array), so I use numpy.fromstring instead.
    
    timedata: First array in ascii file, stand for the photon arrival time(need to be redit here!)
    
    chdata: Second array in ascii file, stand for the channel information.
    
    totalno: The number of photons that arrived the detectored
'''
timedata=np.fromstring(''.join(open('%s.time'%trig,'r').read().splitlines()),sep=' ') # CAUTIONS: Need to give the time file manually
chdata=np.fromstring(''.join(open('%s.channel'%trig,'r').read().splitlines()),sep=' ')
(totalno,)=np.shape(timedata)

n=0 # n is just a temporary variable here, maybe need to be changed if conflict
while n<totalno:
    f=open("%s.time.CH%i"%(trig,chdata[n]),'a')
    f.write("%f"%timedata[n]+'\n')
    f.close()
    n+=1

# <headingcell level=2>

# Do Bayesian Block analysis

# <markdowncell>

# During the analysis, we add Knuth bins ,Scott bins and Freedman bins as comparision.

# <headingcell level=3>

# total data

# <codecell>

#We use standard histogram as background, then Knuth bins & Bayesian block
fig,axes = plt.subplots(2,1,figsize=(12,6))

axes[0].hist(timedata/1000,bins=64,color='blue',histtype='step',label='64ms')
axes[0].set_title('bins=64')
axes[0].set_xlabel('Time/second')
axes[0].set_ylabel('Count')
axes[0].legend(loc='best')


axes[1].hist(timedata/1000,bins=1000,color='blue',histtype='step',normed='True',label='bins=1s')
bbhist(timedata/1000,bins='blocks',color='red',histtype='step',normed='True',label='bayesian')
axes[1].legend(loc='best')
axes[1].set_title('Bayesian block')
axes[1].set_xlabel('Time/second')
axes[1].set_ylabel('Count Rate($s^{-1}$)')
#axes[1].set_ylim([0,0.001])

fig.tight_layout()
fig.savefig('%s.png'%trig,dpi=200)


# <headingcell level=2>

# Channel data

# <headingcell level=3>

# Read Channel data from file

# <codecell>

ch1time=np.genfromtxt('%s.time.CH1'%trig)
ch2time=np.genfromtxt('%s.time.CH2'%trig)
ch3time=np.genfromtxt('%s.time.CH3'%trig)
ch4time=np.genfromtxt('%s.time.CH4'%trig)

(count1,)=ch1time.shape
(count2,)=ch2time.shape
(count3,)=ch3time.shape
(count4,)=ch4time.shape


ch1time=np.reshape(ch1time,[count1,1])
ch2time=np.reshape(ch2time,[count2,1])
ch3time=np.reshape(ch3time,[count3,1])
ch4time=np.reshape(ch4time,[count4,1])

# <headingcell level=3>

# Plot data in one Picture

# <codecell>

fig=plt.figure(figsize=(15,11))

axes=plt.subplot(2,2,1)
axes.hist(ch1time/1000,bins=128,color='blue',normed='True',histtype='step',label='bins=1s')
bbhist(ch1time/1000,bins='blocks',color='red',normed='True',histtype='step',label='bayesian')
axes.legend(loc='best')
axes.set_title('Channel 1')
axes.set_xlabel('Time/second')
axes.set_ylabel('Count Rate($s^{-1}$)')

axes=plt.subplot(2,2,2)
axes.hist(ch2time/1000,bins=64,color='blue',normed='True',histtype='step',label='bins=1s')
bbhist(ch2time/1000,bins='blocks',color='red',normed='True',histtype='step',label='bayesian')
axes.legend(loc='best')
axes.set_title('Channel 2')
axes.set_xlabel('Time/second')
axes.set_ylabel('Count Rate($s^{-1}$)')

axes=plt.subplot(2,2,3)
axes.hist(ch3time/1000,bins=64,color='blue',normed='True',histtype='step',label='bins=1s')
bbhist(ch3time/1000,bins='blocks',color='red',normed='True',histtype='step',label='bayesian')
axes.legend(loc='best')
axes.set_title('Channel 3')
axes.set_xlabel('Time/second')
axes.set_ylabel('Count Rate($s^{-1}$)')

axes=plt.subplot(2,2,4)
axes.hist(ch4time/1000,bins=64,color='blue',normed='True',histtype='step',label='bins=1s')
bbhist(ch4time/1000,bins='blocks',color='red',normed='True',histtype='step',label='bayesian')
axes.legend(loc='best')
axes.set_title('Channel 4')
axes.set_xlabel('Time/second')
axes.set_ylabel('Count Rate($s^{-1}$)')

fig.tight_layout()
fig.savefig('%sCH.png'%trig,dpi=200)

# <codecell>


