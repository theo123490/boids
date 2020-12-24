import simulation as sim
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

birds = sim.Species("birds")
birds.minimal_distance = 3
birds.separation_constant = 10
birds.alignment_constant = 25
birds.maximum_x = 30
birds.maximum_y = 30
birds.minimum_x = -30
birds.minimum_y = -30
birds.add_population(n_of_individual=20, random_range=[[10, 10], [15, 15]])
birds.add_population(n_of_individual=5, random_range=[[5, 5], [0, 0]])
birds.add_population(n_of_individual=20, random_range=[[-10, -10], [-5, -5]])
coordinates = birds.get_coordinates()

fig, ax = plt.subplots()

scat = plt.scatter(coordinates[:,0], coordinates[:,1], s=10)

def update_plot(scat):
    fig.clf()
    birds.move()
    coordinates = birds.get_coordinates()
    scat = plt.scatter(coordinates[:, 0], coordinates[:, 1], s=10)
    plt.xlim(birds.minimum_x, birds.maximum_x)
    plt.ylim(birds.minimum_y, birds.maximum_y)

    return scat

ani = FuncAnimation(fig, update_plot, interval=5)

plt.grid()
plt.show()