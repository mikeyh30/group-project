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
import json

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

# COMSOL simulation
import os
from simulation_wrapper import simulation_wrapper

# Define the input parameters for our function
host = 'monaco'
COMSOL_model = 'ART_res.mph'
paramfile = 'cpw_parameters.txt'
file_gens2 = os.getcwd() + '/downloads/exports/g_ens2.csv'
file_gens2_number = os.getcwd() + '/downloads/exports/g_ens2_number.csv'
file_N = os.getcwd() + '/downloads/exports/N.csv'
w = 2e-06
t = 50e-09
# l = 40e-6
pen = 200e-09
omega = 7.3e09
Z = 50
w_mesa = 4e-07
h_mesa = 5e-08
# gap_ind = 1e-06

# Parameter space
parameter_space = ParameterSpace([ContinuousParameter('l_ind', 10e-06, 50e-06), ContinuousParameter('gap_ind', 4e-07, 2e-06)])

# Function to optimize
def f(X):
    l_ind = X[:, 0]
    gap_ind = X[:, 1]
    out = np.zeros((len(l_ind),1))
    for g in range(len(l_ind)):
        out[g,0] = -simulation_wrapper(host, COMSOL_model, paramfile, w, t, l_ind[g], pen, omega, Z, w_mesa, h_mesa, gap_ind[g])[0]
    return out

#f, space = branin_function()


num_data_points = 10
design = RandomDesign(parameter_space)
X = design.get_samples(num_data_points)
Y = f(X)
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
optimizer = GradientAcquisitionOptimizer(space = parameter_space)
point_calc = SequentialPointCalculator(exp_imprv,optimizer)

bayesopt_loop = BayesianOptimizationLoop(model = model_emukit,
                                         space = parameter_space,
                                         acquisition=exp_imprv,
                                         batch_size=1)

stopping_condition = FixedIterationsStoppingCondition(i_max = 30)
bayesopt_loop.run_loop(f, stopping_condition)


coord_results  = bayesopt_loop.get_results().minimum_location
min_value = bayesopt_loop.get_results().minimum_value
step_results = bayesopt_loop.get_results().best_found_value_per_iteration
print(coord_results)
print(min_value)

results = [coord_results,min_value]

results_file = open('results.txt','w')
results_file.write(str(results))
results_file.close()


data = model_emukit.model.to_dict()
with open('model_data.txt','w') as outfile:
    json.dump(data,outfile)

model_emukit.model.plot(levels=500)
ax = plt.gca()
mappable = ax.collections[0]
plt.colorbar(mappable)
plt.savefig('model.png')
plt.show()

# Shelf
import shelve

filename='/tmp/shelve.out'
my_shelf = shelve.open(filename,'n') # 'n' for new
my_shelf['model_emukit'] = globals()['model_emukit']
# my_shelf['bayesopt_loop']= globals()['bayesopt_loop']
my_shelf.close()

"""
model_emukit.model.plot()
model_emukit.model
plt.show()
print(point_calc)
a = bayesopt_loop.loop_state.X
print(f(a))
plt.scatter(a[:,0],f(a))
plt.show()
print(model_emukit.model)
"""
