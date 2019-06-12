import shelve
import emukit
import matplotlib.pyplot as plt

filename='/tmp/shelve.out'

my_shelf = shelve.open(filename)
for key in my_shelf:
    print(key)
    globals()[key]=my_shelf[key]
my_shelf.close()

# coord_results  = bayesopt_loop.get_results().minimum_location
# print(coord_results)
model_emukit.model.plot(levels = 5)
plt.show()