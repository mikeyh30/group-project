import numpy as np

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
    e_r = 6
    x = s/(s+2*w)
    if x > 0 and x <= 1/(np.sqrt(2)):
        capacitance = (e_r*l*np.log(((-2)/((1-x**2)**(1/4)-1))*((1-x**2)**(1/4)+1)))/(377*np.pi*v_0)
    elif x > 1/(np.sqrt(2)) and x <= 1:
        capacitance = (e_r*l)/(120*v_0*np.log((-2/(np.sqrt(x)-1))*(np.sqrt(x)+1)))
    return capacitance
"""
def inductance(l_ind, w_ind, gap_ind, h_ind, m_r):
    m_0 = 1.256e-06
    s = gap_ind+w_ind
    L = (((m_0*m_r)/(np.pi))*np.arccosh(s/w_ind))*l_ind
    return L
"""

def inductance(l_ind, w_ind, gap_ind, h_ind, m_r):
    #d   diameter
    #h   short side
    #m_r relative permeability

    m_0 = 1.256e-06
    w = l_ind
    h = gap_ind+2*w_ind
    d = 2*w_ind+2*h_ind
    temp = -h*np.log((h+np.sqrt(h**2+w**2))/w)-w*np.log((w+np.sqrt(h**2+w**2))/h)+h*np.log(4*h/d)+w*np.log(4*w/d)
    L = (m_0*m_r/np.pi)*(-2*(w+h)+2*np.sqrt(h**2+w**2)+temp)
    return L

def frequency(L,C):
    freq = 1/(2*np.pi*np.sqrt(L*C))
    return freq

l_ind = 2.28679834e-03
w_ind = 3.84269231e-06
gap_ind = 4.05989377e-07
h_ind = 45e-09
m_r = 1
gap_cap = 3.56391453e-05
w_cap = 4.83137468e-05
l_cap = 8.50854402e-03


print(frequency(inductance(l_ind,w_ind,gap_ind,h_ind,m_r),capacitance(gap_cap,w_cap,l_cap)))