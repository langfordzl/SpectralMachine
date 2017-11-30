#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
*********************************************
*
* MixMaker
* Mix different rruff files into a ASCII
* Files must be in RRuFF
* version: 20171130a
*
* By: Nicola Ferralis <feranick@hotmail.com>
*
***********************************************
'''
print(__doc__)


import numpy as np
import sys, os.path, getopt, glob, csv
from datetime import datetime, date

def main():
    if(len(sys.argv)<4):
        print(' Usage:\n  python3 MixMaker.py <EnIn> <EnFin> <EnStep>\n')
        print(' Requires python 3.x. Not compatible with python 2.x\n')
        return
    else:
        enInit = sys.argv[1]
        enFin =  sys.argv[2]
        enStep = sys.argv[3]
        #threshold = sys.argv[5]

    index = 0
    first = True
    for ind, file in enumerate(sorted(os.listdir("."))):
        try:
            if file[:7] != "mixture" and os.path.splitext(file)[-1] == ".txt":
                with open(file, 'r') as f:
                    En = np.loadtxt(f, unpack = True, usecols=range(0,1), delimiter = ',', skiprows = 10)
                with open(file, 'r') as f:
                    R = np.loadtxt(f, unpack = True, usecols=range(1,2), delimiter = ',', skiprows = 10)
                print(file + '\n File OK, converting to ASCII...')

                EnT = np.arange(float(enInit), float(enFin), float(enStep), dtype=np.float)
            
                if EnT.shape[0] == En.shape[0]:
                    print(' Number of points in the learning dataset: ' + str(EnT.shape[0]))
                else:
                    print('\033[1m' + ' Mismatch in datapoints: ' + str(EnT.shape[0]) + '; sample = ' +  str(En.shape[0]) + '\033[0m')
                    R = np.interp(EnT, En, R, left = 0, right = 0)
                    if first:
                        mixR = R
                        first = False
                    else:
                        mixR = (mixR + R)*index/(index+1)
                    index += 1

                    print('\033[1m' + ' Mismatch corrected: datapoints in sample: ' + str(R.shape[0]) + '\033[0m')
        except:
            pass

    newR = np.transpose(np.vstack((EnT, mixR)))
    newFile = "mixture"+str(datetime.now().strftime('_%Y-%m-%d_%H-%M-%S.txt'))

    with open(newFile, 'ab') as f:
        np.savetxt(f, newR, delimiter='\t', fmt='%10.6f')

    print("\n Mixtures saved in: ",newFile, "\n")

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
