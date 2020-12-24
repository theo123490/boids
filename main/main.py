import simulation as sim
import matplotlib.pyplot as plt


birds = sim.Species("birds")
birds.populate(30, [[ -5, -5], [5, 5]])
coordinates = birds.get_coordinates()
plt.scatter(coordinates[:,0], coordinates[:,1])
plt.show()