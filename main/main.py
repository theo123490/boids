import simulation as sim
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

birds = sim.Species("birds")
birds.minimal_distance = 30
birds.separation_constant = 30
birds.alignment_constant = 0.5
birds.cohesion_constant = 0.05
birds.edge_force_constant = 4
birds.bait_constant = 0.08
birds.speed_limit = 30
birds.maximum_x = 100
birds.maximum_y = 400
birds.minimum_x = -100
birds.minimum_y = -400
birds.vision = 40
birds.add_population(n_of_individual=30, random_range=[[-100, 100], [-400, 400]], velocity_range=[[-100, 100], [-100, 100]])
coordinates = birds.get_coordinates()

span_x = birds.maximum_x - birds.minimum_x
span_y = birds.maximum_y - birds.minimum_y

# plt.figure(1)
# scat = plt.scatter(coordinates[:, 0], coordinates[:, 1], s=30)
# plt.xlim(birds.minimum_x - (span_x * 0.8), birds.maximum_x + (span_x * 0.8))
# plt.ylim(birds.minimum_y - (span_y * 0.8), birds.maximum_y + (span_y * 0.8))
#
# birds.move()
#
# plt.figure(2)
# scat = plt.scatter(coordinates[:, 0], coordinates[:, 1], s=30)
# plt.xlim(birds.minimum_x - (span_x * 0.8), birds.maximum_x + (span_x * 0.8))
# plt.ylim(birds.minimum_y - (span_y * 0.8), birds.maximum_y + (span_y * 0.8))

fig, ax = plt.subplots()
scat = plt.scatter(coordinates[:,0], coordinates[:,1], s=3)
extra_border = 0.4
def update_plot(scat):
    fig.clf()
    birds.move()
    coordinates = birds.get_coordinates()
    scat = plt.scatter(coordinates[:, 0], coordinates[:, 1], s=30)
    plt.xlim(birds.minimum_x - (span_x * extra_border), birds.maximum_x + (span_x * extra_border))
    plt.ylim(birds.minimum_y - (span_y * extra_border), birds.maximum_y + (span_y * extra_border))

    return scat

ani = FuncAnimation(fig, update_plot, interval=50)

plt.grid()
plt.show()