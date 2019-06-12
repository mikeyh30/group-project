#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import csv
import qsd
import qsd.data_processing.setparams as setparams
import os

def capacitance(s,w,l):
    """
    capacitor params
    s   gap
    w   width
    l   length
    e_r relative permittivity
    v_0 speed of light in a vacuum
    excuse the horrible parameter names
    """
    v_0 = 299792548
    e_r = 1
    x = s/(s+2*w)
    if x > 0 and x <= 1/(np.sqrt(2)):
        capacitance = (e_r*l*np.log(((-2)/((1-x**2)**(1/4)-1))*((1-x**2)**(1/4)+1)))/(377*np.pi*v_0)
    elif x > 1/(np.sqrt(2)) and x <= 1:
        capacitance = (e_r*l)/(120*v_0*np.log((-2/(np.sqrt(x)-1))*(np.sqrt(x)+1)))
    return capacitance

# https://www.eeweb.com/tools/rectangle-loop-inductance
def inductance(l_ind, w_ind, gap_ind, h_ind, m_r):
    """
    d   diameter
    h   short side
    m_r relative permeability
    """
    m_0 = 1.256e-06
    w = l_ind
    h = gap_ind+2*w_ind
    d = 2*w_ind+2*h_ind
    temp = -h*np.log((h+np.sqrt(h**2+w**2))/w)-w*np.log((w+np.sqrt(h**2+w**2))/h)+h*np.log(4*h/d)+w*np.log(4*w/d)
    L = (m_o*m_r/np.pi)*(-2*(w+h)+2*np.sqrt(h**2+w**2)+temp)
    return L

def impedance(L,C):
    Z = np.sqrt(L/C)
    return Z

def frequency(L,C):
    f = 1/np.sqrt((2*np.pi*L*C))
    return f

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
    gap_cap = float(pd["gap_cap"])
    w_cap = float(pd["w_cap"])
    l_cap = float(pd["l_cap"])
    w_mesa = float(pd["w_mesa"])
    h_mesa = float(pd["h_mesa"])
    gap_ind = float(pd["gap_ind"])
    inductance =inductance(l,w,gap_ind,t,0.001)
    capacitance=capacitance(gap_cap, w_cap, l_cap)
    Z = impedance(inductance,capacitance)
    print(Z)

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
    return currentDensityFile, paramlistfilename, frequency(inductance,capacitance)

if __name__ == "__main__":
    preprocess("cpw_parameters.txt")