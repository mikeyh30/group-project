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

f, space = branin_function()

param_space = ParameterSpace([ContinuousParameter('x1',0,10),ContinuousParameter('x2',0,15)])

num_data_points = 30
design = RandomDesign(param_space)
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

model_emukit.model.plot()
model_emukit.model
plt.show()

exp_imprv = ExpectedImprovement(model = model_emukit)
optimizer = GradientAcquisitionOptimizer(space = param_space)
point_calc = SequentialPointCalculator(exp_imprv,optimizer)

bayesopt_loop = BayesianOptimizationLoop(model = model_emukit,
                                         space = param_space,
                                         acquisition=exp_imprv,
                                         batch_size=5)

stopping_condition = FixedIterationsStoppingCondition(i_max = 100)
bayesopt_loop.run_loop(f, stopping_condition)
coord_results  = bayesopt_loop.get_results().minimum_location
min_value = bayesopt_loop.get_results().minimum_value
step_results = bayesopt_loop.get_results().best_found_value_per_iteration
print(coord_results)
print(min_value)
print(step_results)
plt.plot(step_results)
plt.show()
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
