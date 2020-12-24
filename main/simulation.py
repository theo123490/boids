import numpy as np

class Individual:
    def __init__(self, initial_x, initial_y, species):
        self.x = initial_x
        self.y = initial_y
        self.species = species
        self.separation = 0

    def move(self, move_x, move_y):
        self.x += move_x
        self.y += move_y

    def location(self):
        print("current location is in x: {} y: {}".format(self.x, self.y))

    def calculate_separation(self, separation_constant, group):
        group_x = group[:,0]
        group_y = group[:,1]
        self.separation = [np.mean(group_x), np.mean(group_y)]

class Species:
    def __init__(self, species_name):
        self.species_name = species_name
        self.group = []
        self.center = None

    def populate(self, n_of_individual, random_range):
        x_min = random_range[0][0]
        y_min = random_range[0][1]
        x_max = random_range[1][0]
        y_max = random_range[1][1]
        x_coordinates = np.random.uniform(low=x_min, high=x_max, size=n_of_individual)
        y_coordinates = np.random.uniform(low=y_min, high=y_max, size=n_of_individual)
        for n in range(n_of_individual):
            self.group.append(Individual(initial_x=x_coordinates[n], initial_y=y_coordinates[n], species=self.species_name))

    def get_coordinates(self):
        coordinates = []
        for individual in self.group:
            coordinates.append([individual.x, individual.y])
        coordinates = np.array(coordinates)
        return coordinates