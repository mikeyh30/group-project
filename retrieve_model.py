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
model_emukit.model.plot(levels = 500,visible_dims=[0,3])
ax = plt.gca()
mappable = ax.collections[0]
plt.colorbar(mappable)
plt.savefig('model.png')
plt.show()