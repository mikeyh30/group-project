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

# Define the input parameters for our functions
host = 'monaco'
COMSOL_model = 'ART_res.mph'
paramfile = 'cpw_parameters.txt'
file_gens2 = os.getcwd() + '/downloads/exports/g_ens2.csv'
file_gens2_number = os.getcwd() + '/downloads/exports/g_ens2_number.csv'
file_N = os.getcwd() + '/downloads/exports/N.csv'
#w = 2.4e-06
t = 45e-09
# l = 240e-6
# gap_ind = 2.4e-06
pen = 200e-09
omega = 7.03e09
# gap_cap = 60e-06
# w_cap = 45e-06
# l_cap = 2500e-06
w_mesa = 4e-07
h_mesa = 45e-09

# Number of simulation runs
no_random_seeds = 50
no_BO_sims = 500

# Parameter space
parameter_space = ParameterSpace([\
    ContinuousParameter('gap_cap', 1e-06, 1e-04), \
    ContinuousParameter('w_cap', 1e-06, 1e-04),\
    ContinuousParameter('l_cap', 1e-04, 1e-02), \
    ContinuousParameter('l_ind', 1e-04, 1e-02),
    ContinuousParameter('w', 1e-08, 1e-05),\
    ContinuousParameter('gap_ind', 1e-08, 1e-06),\
    ])

# Function to optimize
def q(X):
    gap_cap = X[:,0]
    w_cap = X[:,1]
    l_cap = X[:,2]
    l_ind = X[:,3]
    w = X[:,4]
    gap_ind = X[:,5]
    out = np.zeros((len(l_ind),1))
    for g in range(len(l_ind)):
        # Check that resonator geometry is sensible:
        if l_ind[g] > l_cap[g]/2:
            out[g,0] = 10e20 #Large cost to bad geometry
        else:
            out[g,0] = -simulation_wrapper(host, COMSOL_model, paramfile, w[g], t, l_ind[g], pen, omega, gap_cap[g], w_cap[g], l_cap[g], w_mesa, h_mesa, gap_ind[g])[0]
    return out

# Set up random seeding of parameter space
num_data_points = no_random_seeds
design = RandomDesign(parameter_space)
X = design.get_samples(num_data_points)
Y = q(X)

# Set up emukit model
model_gpy = GPRegression(X,Y)
model_gpy.optimize()
model_emukit = GPyModelWrapper(model_gpy)

# Set up Bayesian optimisation routine
exp_imprv = ExpectedImprovement(model = model_emukit)
optimizer = GradientAcquisitionOptimizer(space = parameter_space)
point_calc = SequentialPointCalculator(exp_imprv,optimizer)

# Bayesian optimisation routine
bayesopt_loop = BayesianOptimizationLoop(model = model_emukit,
                                         space = parameter_space,
                                         acquisition=exp_imprv,
                                         batch_size=1)

stopping_condition = FixedIterationsStoppingCondition(i_max = no_BO_sims)
bayesopt_loop.run_loop(q, stopping_condition)


# Results of Bayesian optimisation
coord_results  = bayesopt_loop.get_results().minimum_location
min_value = bayesopt_loop.get_results().minimum_value
step_results = bayesopt_loop.get_results().best_found_value_per_iteration
print(coord_results)
print(min_value)

# Save the pararmeters of the best resonator
results = [coord_results,min_value]
results_file = open('results.txt','w')
results_file.write(str(results))
results_file.close()

# Save the entire results of the model
data = model_emukit.model.to_dict()
with open('model_data.txt','w') as outfile:
    json.dump(data,outfile)

# Plotting
model_emukit.model.plot(levels=500,visible_dims=[1,2])
ax = plt.gca()
mappable = ax.collections[0]
plt.colorbar(mappable)
plt.savefig('model.png')
plt.show()

# Shelve - Can import the model easily using the retrieve_model.py file
import shelve
filename='/tmp/shelve.out'
my_shelf = shelve.open(filename,'n') # 'n' for new
my_shelf['model_emukit'] = globals()['model_emukit']
# my_shelf['bayesopt_loop']= globals()['bayesopt_loop']
my_shelf.close()