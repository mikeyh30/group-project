#!/usr/bin/env python

from scipy import constants as sp
import os
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
import csv
from qsd.data_processing import readcomsol,postproc
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from scipy import interpolate

file_gens2 = os.getcwd() + '/qsd/downloads/exports/g_ens2.csv'
file_gens2_number = os.getcwd() + '/qsd/downloads/exports/g_ens2_number.csv'
file_N = os.getcwd() + '/qsd/downloads/exports/N.csv'

def return_COMSOL_table(file):
    x = []
    with open(file, 'r') as rf:
        reader = csv.reader(rf, delimiter=',')
        for i in range(5):
            next(reader) #Get rid of header rows
        row = [row for row in reader] #Extract from csvreader object
        for column in row[0]:#Only valid for 1 row csv
            x.append(column)
    x = np.asarray((x),dtype=float)
    x = x[::-1]
    x = make_cumulative(x)
    return x

def make_cumulative(array):
    for i in range(len(array)-1,0,-1):
        array[i-1] = array[i-1] + array[i]
    return array

def postprocess(gens_file):
    gens = np.sqrt(return_COMSOL_table(gens_file))
    FWHM = 0 #Need to make function which calculates FWHM
    return gens, FWHM

N = return_COMSOL_table(file_N)
gens2 = return_COMSOL_table(file_gens2)
gens, FWHM = postprocess(file_gens2_number)
print(gens)

y = [i for i in np.arange(0,0.1+0.01,0.01)]
y.append(0.15)
y.extend([i for i in np.arange(0.2,2,0.1)])


fig0, ax0 = plt.subplots(figsize=(6,4))
ax0.plot(y,np.sqrt(gens2))
ax0.set_xlabel('$g_{{0min}}$',fontsize='24')
ax0.set_ylabel('$g_{{ens}}$',fontsize='24')
# plt.tight_layout()
# plt.savefig(str(os.getcwd() + '/figs/' + 'theta_density.eps'))
# plt.show()

fig1, ax1 = plt.subplots(figsize=(6,4))
ax1.plot(y[1:],N[1:])
ax1.set_xlabel('$g_{{0min}}$',fontsize='24')
ax1.set_ylabel('$N$',fontsize='24')
# plt.tight_layout()
# plt.savefig(str(os.getcwd() + '/figs/' + 'theta_density.eps'))
# plt.show()

f_gens = interpolate.UnivariateSpline(y,np.sqrt(gens2),s=100)
f_N = interpolate.UnivariateSpline(y,N,s=100)
dfg = f_gens.derivative()
dfn = f_N.derivative()

fig2, ax2 = plt.subplots(figsize=(10,8))
ax2.plot(y[1:],dfn(y[1:]))
ax2.set_xlabel('$g_{{0min}}$',fontsize='24')
ax2.set_ylabel('$dg/dn$',fontsize='24')
# plt.tight_layout()
# plt.savefig(str(os.getcwd() + '/figs/' + 'theta_density.eps'))
plt.show()


