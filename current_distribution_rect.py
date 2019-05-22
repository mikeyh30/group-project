import numpy as np
import matplotlib.pyplot as plt

# from T. Van Duzer and C. Turner, Superconductive Devices and Circuits (Prentice Hall PTR, 1999)
# haven't actually checked the ref but just found from Reaching the quantum limit of sensitivity
# in electron spin resonance SI and ripped off ref.
def J(x, w, t, pen):
    ans = []
    for i in x:
        if abs(i) > w/2.:
            ans.append(0)
        elif abs(i) == w/2.:
            ans.append(1.165/pen*(w*t)**.5)
        elif abs(i) < w/2. and abs(i) > w/2. - pen**2/(2*t):
            ans.append(1.165/pen*(w*t)**.5*np.exp(-(w/2. - abs(i))*t/pen**2))
        else:
            ans.append((1 - (2*abs(i)/w)**2)**-.5)
    return np.asarray(ans)
    
# def field( 
        
#constants
hbar = 1.054e-34

# define the superconductor
w = 2e-6
t = 50e-9
pen = 290e-9

#define the resonator - from CST or experiment
omega = 8e9*2*np.pi
Z = 326

#define the 'mesh'
x = np.linspace(-.55*w, .55*w, 1000)

#solve for currents - not normalised
Js = J(x, w, t, pen)

#normalise 
dI = omega*(hbar/(2*Z))**.5
dx = x[1] - x[0]
Jnorm = dI*Js/(t*dx*np.sum(Js))

#Plot the result
fig, ax = plt.subplots(figsize=(6,4))
ax.plot(x*1e6, Jnorm)
ax.set_xlabel('Distance across wire ($\mu$m)', fontsize='large')
ax.set_ylabel('Current density (Am$^{-2}$)', fontsize='large')
plt.tight_layout()
plt.show()

#find fields at depth d
d = 100e-9


np.savetxt(r'current_2um_con_326ohm.txt', np.asarray([x,Jnorm]).transpose())