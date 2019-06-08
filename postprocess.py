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
    #x = make_cumulative(x)
    return x

def make_cumulative(array):
    for i in range(len(array)-1,0,-1):
        array[i-1] = array[i-1] + array[i]
    return array

def postprocess(gens_file):
    gens = np.sqrt(return_COMSOL_table(gens_file))
    FWHM = 0 #Need to make function which calculates FWHM
    return gens, FWHM

def plot_n():
    fig1, ax1 = plt.subplots(figsize=(6,4))
    ax1.plot(y[1:],N[1:],y[1:],f_N(y[1:]))
    ax1.set_xlabel('$g_{{0min}}$',fontsize='24')
    ax1.set_ylabel('$N$',fontsize='24')
    plt.show()

def plot_interp_n():
    # This shows the weighted gens
    fig2, ax2 = plt.subplots(figsize=(10,8))
    # ax2.plot(np.arange(0,2,0.01),np.multiply(dfg2(np.arange(0,2,0.01)),dfn(np.arange(0,2,0.01))))
    x = np.arange(0,2,0.01)
    ax2.plot(x,f_N(x),y,N)
    ax2.set_xlabel('$g_{{0min}}$',fontsize='24')
    ax2.set_ylabel('$N$',fontsize='24')
    ax2.set_ylim(-1e5,5e7)
    plt.show()

def plot_gens():
    fig0, ax0 = plt.subplots(figsize=(6,4))
    ax0.plot(y,np.sqrt(gens2),y,f_gens(y))
    ax0.set_xlabel('$g_{{0min}}$',fontsize='24')
    ax0.set_ylabel('$g_{{ens}}$',fontsize='24')
    plt.show()

def plot_derivative_gens():
    # This shows just the derivative of gens
    fig2, ax2 = plt.subplots(figsize=(10,8))
    ax2.plot(np.arange(0,2,0.01),-dfg(np.arange(0,2,0.01)),np.arange(0,2,0.01),-dfg2(np.arange(0,2,0.01)))
    ax2.set_xlabel('$g_{{0min}}$',fontsize='24')
    ax2.set_ylabel('$dge/dg0 * N$',fontsize='24')
    plt.show()

if __name__ == "__main__":
    file_gens2 = os.getcwd() + '/downloads/exports/g_ens2.csv'
    file_gens2_number = os.getcwd() + '/downloads/exports/g_ens2_number.csv'
    file_N = os.getcwd() + '/downloads/exports/N.csv'

    N = return_COMSOL_table(file_N)
    gens2 = return_COMSOL_table(file_gens2)
    gens, FWHM = postprocess(file_gens2_number)
    print(gens[0])

    y = [i for i in np.arange(0,0.1+0.01,0.01)]
    y.append(0.15)
    y.extend([i for i in np.arange(0.2,1.4,0.1)])
    y.extend([i for i in np.arange(1.4,1.99,0.2)])
    bins1 = y + [2]
    binmid=[]
    [binmid.append(0.5*(bins1[i]+bins1[i+1])) for i in range(len(y))]

    f_gens = interpolate.UnivariateSpline(y,np.sqrt(gens2),s=100)
    f_gens2= interpolate.UnivariateSpline(y,np.sqrt(gens2),s=20000000)
    f_N = interpolate.UnivariateSpline(y,N,s=1)
    f_N2= interpolate.UnivariateSpline(y,N,s=100000000000)
    dfg = f_gens.derivative()
    dfg2=f_gens2.derivative()
    dfn = f_N2.derivative()
    # weighted_diffg = dfg*f_N

    # plot_n()
    plot_interp_n()
    # plot_gens()
