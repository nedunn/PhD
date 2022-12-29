'''
This will take the files will are given an identifying number automatically by LightField
and move the number to the head of the file.
'''
#! /usr/bin/python

import os
import pandas as pd
import glob

indir='/mnt/c/Users/16162/Documents/Data/2022-12-09/0_original/'
outdir='/mnt/c/Users/16162/Documents/Data/2022-12-09/0_rawFrames/'


def newname(oldname):
    dropcsv=oldname.split('.csv')[0]
    baseWnum=dropcsv.split('-Fr')[0]
    framenum=dropcsv.split('-Frame-')[1]
    splits=baseWnum.split(' ')
    result=splits[1]+'_'+splits[0]+'-Frame-'+framenum+'.csv'
    return result

if __name__ == '__main__':
    for file in os.listdir(indir):
        df=pd.read_csv(indir+file,header=None)
        df.to_csv(outdir+newname(file),index=False,header=False)
        

