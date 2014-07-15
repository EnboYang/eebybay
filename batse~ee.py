# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 20:23:17 2014

@author: enboyang
license: GPLv2
"""
import numpy as np
import matplotlib.pyplot as plt
from astroML.plotting import hist as bbhist
import linecache

# This function is used to create related file to preserve the data
def filecreate(trig):
    f=open('%s.time'%trig,'w')
    f.close()
    f=open('%s.channel'%trig,'w')
    f.close()
    f=open('%s.detector'%trig,'w')
    f.close()
    # read and preserve header data, it contains npts which is the total count of
    # photons that detected.
    f=open('%s.header'%trig,'wa')
    headerdata=linecache.getline('tteascii.%s'%trig,2)
    f.write(headerdata)
    f.close()
    chnum=1
    while chnum<=4:
        f=open("%s.time.CH%s"%(trig,chnum),'w')
        f.close()
        chnum+=1

# This function is used to split different types of data and preserved them to specific file
def datawrite(trig):
    npts=np.genfromtxt('%s.header'%trig,dtype=int)
    npts=int(npts[2])    
    linenum=len(open('tteascii.%s'%trig,'r').readlines())#读入文件总行数
    headline=5
    timeline=headline+npts/10+1
    chline=timeline+npts/40+1
    i=headline+1
    f=open('%s.time'%trig,'a')
    while i<=timeline:
        timedata=linecache.getline('tteascii.%s'%trig,i)
        f.write(timedata)
        i+=1
    f.close()
    i=timeline+1
    f=open('%s.channel'%trig,'a')
    while i<=chline:
        chdata=linecache.getline('tteascii.%s'%trig,i)
        f.write(chdata)
        i+=1
    f.close()
    i=chline+1
    f=open('%s.detector'%trig,'a')
    while i<=linenum:
        detecdata=linecache.getline('tteascii.%s'%trig,i)
        f.write(detecdata)
        i+=1
    f.close()

# This function is used to draw picture with bin=64ms, 1s and bayesian blocks analysis
def drawpic(trig):
    timedata=np.fromstring(''.join(open('%s.time'%trig,'r').read().splitlines()),sep=' ')
    fig,axes=plt.subplots(2,1,figsize=(9,6))
    axes[0].hist(timedata/1000000,bins=64,color='blue',histtype='step',label='64ms')
    axes[0].set_title('%s'%trig)
    axes[0].set_xlabel('Time/second')
    axes[0].set_ylabel('Count')
    axes[0].legend(loc='best')
    axes[1].hist(timedata/1000000,bins=1000,color='blue',histtype='step',normed='True',label='bins=1s')
    bbhist(timedata/1000000,bins='blocks',color='red',histtype='step',normed='True',label='bayesian')
    axes[1].legend(loc='best')
    axes[1].set_title('Bayesian block&1s')
    axes[1].set_xlabel('Time/second')
    axes[1].set_ylabel('Count Rate($s^{-1}$)')
    axes[1].set_ylim([0,4])
    fig.tight_layout()
    fig.savefig('%s.png'%trig,dpi=200)
    
        

#Main program, we use a loop and call functions here.
trignum=np.genfromtxt('trig.dat',dtype=str)
totaltrig=trignum.size
i=0
while i< totaltrig:
    filecreate(trignum[i])
    datawrite(trignum[i])
    drawpic(trignum[i])
    i+=1

