#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import csv
import qsd
import qsd.data_processing.setparams as setparams
import os

def preprocess(paramfilename):
    # Define geometry of the superconductor
    paramfile=open(paramfilename,"r")
    filestring = paramfile.read()
    filelist = filestring.split("\n")

    pd = {}
    for fl in filelist:
        l = fl.split()
        pd[l[0]] = l[2]
    paramfile.close()

    w = float(pd["w"])
    t = float(pd["t"])
    l = float(pd["l"])
    pen = float(pd["pen"])
    omega = float(pd["omega"])
    Z = float(pd["Z"])

    setp = setparams.SetParams()#w,t,l,pen,omega,Z)
    params = setp.set_params(paramfilename)

    # Define the 'mesh'
    x = np.linspace(-w, w, int(1e04))

    # Instantiate Special CPW object
    cpw = qsd.electromagnetics.CPW(x,l,w,t,pen,Z,omega)

    # Js = cpw.J() #s Current density - not normalised
    Jnorm = cpw.normalize_J() # Normalise 
    I = cpw.current(norm='no') # Current
    # E = cpw.E() # Electric field
    # sigma = cpw.conductivity() # Conductivity

    # Generate a parameter list for COMSOL modelling
    paramlist = setp.param_list(x,I,Jnorm,"qsd_gpm/paramlist.txt") # Generate COMSOL parameter list
    paramlistfilename = str(os.getcwd() + "/qsd_gpm/paramlist.txt")

    # Save data to csv file
    currentDensityFile = str(os.getcwd() + "/qsd_gpm/current_density.csv")
    np.savetxt(currentDensityFile, np.column_stack((x,Jnorm)), delimiter=",")
    return currentDensityFile, paramlistfilename

if __name__ == "__main__":
    preprocess("cpw_parameters.txt")