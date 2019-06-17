import shelve
import emukit
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

filename='/tmp/shelve.out'

my_shelf = shelve.open(filename)
for key in my_shelf:
    print(key)
    globals()[key]=my_shelf[key]
my_shelf.close()

# coord_results  = bayesopt_loop.get_results().minimum_location
# print(coord_results)
# model_emukit.model.plot(levels = 5,visible_dims=[1,2])
# plt.title(r'$g_{\mathrm{ens}}$')
# ax = plt.gca()
# mappable = ax.collections[0]
# plt.colorbar(mappable)
# plt.savefig('model.png')
# plt.show()


# Select features to include in the plot
plot_feat = [r'$\mathrm{gap}_{\mathrm{cap}}$', r'$\mathrm{w}_{\mathrm{cap}}$', r'$\mathrm{l}_{\mathrm{cap}}$', r'$\mathrm{l}_{\mathrm{ind}}$', r'$\mathrm{w}_{\mathrm{ind}}$', r'$\mathrm{gap}_{\mathrm{ind}}$']

x = model_emukit.X
X = np.array(x)
X_norm = pd.DataFrame(X,columns = plot_feat)
y = model_emukit.Y
Y = np.array(y)
Y_frame = pd.DataFrame(Y,columns = ['swag'])


normalized_X=(X_norm-X_norm.min())/(X_norm.max()-X_norm.min())

# Concat classes with the normalized data
data_norm = pd.concat([normalized_X[plot_feat], Y_frame], axis=1)
data = data_norm.nsmallest(5, 'swag')
# Perform parallel coordinate plot
ax = pd.plotting.parallel_coordinates(data,'swag')
# ax.get_legend().remove()
plt.title(r'Best 5 normalized parameter sets')
plt.show()