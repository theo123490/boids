import numpy as np
import sys

class Individual:
    def __init__(self, initial_x, initial_y, species, index, minimal_distance=0):
        self.x = initial_x
        self.y = initial_y
        self.species = species
        self.minimal_distance = minimal_distance
        self.index = index
        self.separation_velocity = [0,0]
        self.x_velocity = 0
        self.y_velocity = 0
        self.alignment_velocity = 0

    def set_species(self, species):
        self.species = species

    def move(self, move_x, move_y):
        self.x += move_x
        self.y += move_y

        if self.x > self.species.maximum_x:
            self.x = self.species.maximum_x - np.abs(move_x)
            self.x_velocity = -1 * self.x_velocity
        elif self.y > self.species.maximum_y:
            self.y = self.species.maximum_y - np.abs(move_y)
            self.y_velocity = -1 * self.y_velocity
        elif self.x < self.species.minimum_x:
            self.x = self.species.minimum_x + np.abs(move_x)
            self.x_velocity = -1 * self.x_velocity
        elif self.y < self.species.minimum_y:
            self.y = self.species.minimum_y + np.abs(move_y)
            self.y_velocity = -1 * self.y_velocity

    def location(self):
        print("current location is in x: {} y: {}".format(self.x, self.y))

    def calculate_distance(self, x, y):
        return np.sqrt(np.abs(x - self.x) ** 2 + np.abs(y - self.y) ** 2)

    def calculate_individual_separation(self, other_individual):
        separation = [0,0]
        distance = self.calculate_distance(other_individual.x, other_individual.y)
        if (distance < self.minimal_distance):
            distance_x = other_individual.x - self.x
            distance_y = other_individual.y - self.y
            distance_radian = np.arctan2(distance_y, distance_x)
            separation_velocity = self.minimal_distance - distance
            separation_x = np.cos(distance_radian) * separation_velocity * -1
            separation_y = np.sin(distance_radian) * separation_velocity * -1
            separation = [separation_x, separation_y]

        return separation

    def calculate_separation_velocity(self):
        separation_vectors_x = []
        separation_vectors_y = []
        for i in self.species.group:
            if (i.index == self.index):
                continue
            else:
                individual_separation = self.calculate_individual_separation(i)
                separation_vectors_x.append(individual_separation[0])
                separation_vectors_y.append(individual_separation[1])
        self.separation_velocity = [np.mean(separation_vectors_x), np.mean(separation_vectors_y)] * self.species.separation_constant

    def calculate_alignment_velocity(self):
        group_velocities_x = []
        group_velocities_y = []
        for i in self.species.group:
            group_velocities_x.append(i.x)
            group_velocities_y.append(i.y)

        self.alignment_velocity = [np.mean(group_velocities_x)/len(group_velocities_x), np.mean(group_velocities_y)/len(group_velocities_y)] * self.species.alignment_constant

    def calculate_next_move(self):
        self.calculate_separation_velocity()
        self.calculate_alignment_velocity()
        self.x_velocity = self.separation_velocity[0] + self.alignment_velocity[0]
        self.y_velocity = self.separation_velocity[1] + self.alignment_velocity[1]

    def next_frame(self):
        self.move(self.x_velocity, self.y_velocity)

class Species:
    def __init__(self, species_name):
        self.species = species_name
        self.group = []
        self.center = None
        self.minimal_distance = 0
        self.maximum_x = sys.maxsize
        self.maximum_y = sys.maxsize
        self.minimum_x = -1 * sys.maxsize
        self.minimum_y = -1 * sys.maxsize
        self.separation_constant = 1
        self.alignment_constant = 1
        self.cohesion_constant = 1


    def add_population(self, n_of_individual, random_range):
        x_min = random_range[0][0]
        y_min = random_range[0][1]
        x_max = random_range[1][0]
        y_max = random_range[1][1]
        x_coordinates = np.random.uniform(low=x_min, high=x_max, size=n_of_individual)
        y_coordinates = np.random.uniform(low=y_min, high=y_max, size=n_of_individual)
        for n in range(n_of_individual):
            individual = Individual(initial_x=x_coordinates[n], initial_y=y_coordinates[n], species=self, index=np.random.randint(-sys.maxsize, sys.maxsize), minimal_distance=self.minimal_distance)
            self.group.append(individual)

    def get_coordinates(self):
        coordinates = []
        for individual in self.group:
            coordinates.append([individual.x, individual.y])
        coordinates = np.array(coordinates)
        return coordinates

    def calculate_next_move(self):
        for individual in self.group:
            individual.calculate_next_move()

    def move(self):
        self.calculate_next_move()
        for individual in self.group:
            individual.next_frame()
