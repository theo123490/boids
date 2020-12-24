import simulation as sim
import matplotlib.pyplot as plt


birds = sim.Species("birds")
birds.populate(n_of_individual=20, random_range=[[ -5, -5], [5, 5]], separation_constant=5)

plt.figure(1)
coordinates = birds.get_coordinates()
plt.scatter(coordinates[:,0], coordinates[:,1])

birds.move()

plt.figure(2)
coordinates_a = birds.get_coordinates()
plt.scatter(coordinates_a[:,0], coordinates_a[:,1])

birds.move()

plt.figure(3)
coordinates_b = birds.get_coordinates()
plt.scatter(coordinates_b[:,0], coordinates_b[:,1])

plt.show()