import simulation as sim
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

birds = sim.Species("birds")
birds.populate(n_of_individual=100, random_range=[[-5, -5], [5, 5]], separation_constant=15)
coordinates = birds.get_coordinates()

fig, ax = plt.subplots()
ax.set_xlim(-30, 30)
ax.set_ylim(-30, 30)

scat = plt.scatter(coordinates[:,0], coordinates[:,1], s=10)

def update_plot(scat):
    fig.clf()
    birds.move()
    coordinates = birds.get_coordinates()
    scat = plt.scatter(coordinates[:, 0], coordinates[:, 1], s=10)
    plt.xlim(-30, 30)
    plt.ylim(-30, 30)

    return scat,

ani = FuncAnimation(fig, update_plot)

plt.grid()
plt.show()