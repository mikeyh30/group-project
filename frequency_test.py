from emukit.test_functions import branin_function
from emukit.core import ParameterSpace, ContinuousParameter
from emukit.experimental_design.model_free.random_design import RandomDesign
from GPy.models import GPRegression
from emukit.model_wrappers import GPyModelWrapper
from emukit.model_wrappers.gpy_quadrature_wrappers import BaseGaussianProcessGPy, RBFGPy
import numpy as np
import GPy
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

# Decision loops
from emukit.experimental_design.model_based import ExperimentalDesignLoop
from emukit.bayesian_optimization.loops import BayesianOptimizationLoop
from emukit.quadrature.loop import VanillaBayesianQuadratureLoop

# Acquisition functions
from emukit.bayesian_optimization.acquisitions import ExpectedImprovement
from emukit.experimental_design.model_based.acquisitions import ModelVariance
from emukit.quadrature.acquisitions import IntegralVarianceReduction

# Acquistions optimizers
from emukit.core.optimization import GradientAcquisitionOptimizer

# Stopping conditions
from emukit.core.loop import FixedIterationsStoppingCondition

# Point calculator
from emukit.core.loop import SequentialPointCalculator

# Bayesian quadrature kernel and model
from emukit.quadrature.kernels import QuadratureRBF
from emukit.quadrature.methods import VanillaBayesianQuadrature

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


#w = 2.4e-06
t = 45e-09
# l = 240e-6
pen = 200e-09
omega = 7.03e09
#gap_cap = 1e-06
# w_cap = 45e-06
#l_cap = 2500e-06
w_mesa = 4e-07
h_mesa = 45e-09
# gap_ind = 2.4e-06

param_space = ParameterSpace([\
    ContinuousParameter('gap_cap', 1e-06, 1e-04), \
    ContinuousParameter('w_cap', 1e-06, 1e-04),\
    ContinuousParameter('l_cap', 1e-04, 1e-02), \
    ContinuousParameter('l', 1e-04, 1e-02),
    ContinuousParameter('w', 1e-08, 1e-05),\
    ContinuousParameter('gap_ind', 1e-08, 1e-06),\
    #ContinuousParameter('l_cap', 150e-06, 750e-06)
    ])
# Function to optimize

def min_freq(X):
    gap_cap = X[:,0]
    w_cap = X[:,1]
    l_cap = X[:,2]
    l = X[:,3]
    w = X[:,4]
    gap_ind = X[:,5]
    #gap_cap=4.5e-05
    #w_cap=3e-005
    #w=1e-06
    #gap_ind=5e-08
    t = 45e-09
    f_res = 7e09
    #l_cap = 2500e-06
    out = np.zeros((len(l_cap),1))
    for g in range(len(l_cap)):
        if l[g] > l_cap[g]/2:
            out[g,0] = 10e20
        else:
            C = capacitance(gap_cap[g], w_cap[g], l_cap[g])
            L = inductance(l[g],w[g],gap_ind[g],t,1)
            freq = frequency(L,C)
            print(freq)
            if freq > 6.5e09 and freq < 7.5e09:
                out[g,0] = 0 # Negative as want to optimize against this
            else:
                out[g,0] = abs(freq-f_res)
    return out

num_data_points = 10
design = RandomDesign(param_space)
X = design.get_samples(num_data_points)
Y = min_freq(X)
"""
num_data_points = 1000
design = RandomDesign(param_space)
X = design.get_samples(num_data_points)
Y = f(X)
plt.plot(X,Y)
plt.show()
"""
model_gpy = GPRegression(X,Y)
model_gpy.optimize()
model_emukit = GPyModelWrapper(model_gpy)
"""
model_emukit.model.plot()
model_emukit.model
plt.show()
"""
exp_imprv = ExpectedImprovement(model = model_emukit)
optimizer = GradientAcquisitionOptimizer(space = param_space)
point_calc = SequentialPointCalculator(exp_imprv,optimizer)

bayesopt_loop = BayesianOptimizationLoop(model = model_emukit,
                                         space = param_space,
                                         acquisition=exp_imprv,
                                         batch_size=1)

stopping_condition = FixedIterationsStoppingCondition(i_max = 100)
bayesopt_loop.run_loop(min_freq, stopping_condition)
coord_results  = bayesopt_loop.get_results().minimum_location
min_value = bayesopt_loop.get_results().minimum_value
step_results = bayesopt_loop.get_results().best_found_value_per_iteration
print(coord_results)
print("%.4g" % min_value)
model_emukit.model.plot(levels=50,visible_dims=[1,2])
ax = plt.gca()
#mappable = ax.collections[0]
#plt.colorbar(mappable)
#plt.savefig('model.png')
plt.show()
#print(step_results)
#plt.plot(step_results)
#plt.show()
