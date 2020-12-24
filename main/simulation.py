import numpy as np

class Individual:
    def __init__(self, initial_x, initial_y, species, index, separation_constant=0):
        self.x = initial_x
        self.y = initial_y
        self.species = species
        self.separation_constant = separation_constant
        self.index = index
        self.separation_force = [0,0]
        self.group = None
        self.x_force = 0
        self.y_force = 0

    def set_group(self, group):
        self.group = group

    def move(self, move_x, move_y):
        self.x += move_x
        self.y += move_y

    def location(self):
        print("current location is in x: {} y: {}".format(self.x, self.y))

    def calculate_distance(self, x, y):
        return np.sqrt(np.abs(x - self.x) ** 2 + np.abs(y - self.y) ** 2)

    def calculate_individual_separation(self, other_individual):
        separation = [0,0]
        distance = self.calculate_distance(other_individual.x, other_individual.y)
        if (distance < self.separation_constant):
            distance_x = other_individual.x - self.x
            distance_y = other_individual.y - self.y
            radian = np.arctan2(distance_y, distance_x)
            separation_force_distance = self.separation_constant - distance
            separation_x = np.cos(radian) * separation_force_distance * -1
            separation_y = np.sin(radian) * separation_force_distance * -1
            separation = [separation_x, separation_y]

        return separation

    def calculate_separation_force(self):
        separation_vectors_x = []
        separation_vectors_y = []
        for i in self.group:
            if (i.index == self.index):
                continue
            else:
                individual_separation = self.calculate_individual_separation(i)
                separation_vectors_x.append(individual_separation[0])
                separation_vectors_y.append(individual_separation[1])
        self.separation_force = [np.mean(separation_vectors_x), np.mean(separation_vectors_y)]

    def calculate_next_move(self):
        self.calculate_separation_force()
        self.x_force = self.separation_force[0]
        self.y_force = self.separation_force[1]

    def next_frame(self):
        self.move(self.x_force, self.y_force)



class Species:
    def __init__(self, species_name):
        self.species_name = species_name
        self.group = []
        self.center = None
        self.separation = 0

    def populate(self, n_of_individual, random_range, separation_constant=0):
        x_min = random_range[0][0]
        y_min = random_range[0][1]
        x_max = random_range[1][0]
        y_max = random_range[1][1]
        self.separation = separation_constant
        x_coordinates = np.random.uniform(low=x_min, high=x_max, size=n_of_individual)
        y_coordinates = np.random.uniform(low=y_min, high=y_max, size=n_of_individual)
        for n in range(n_of_individual):
            individual = Individual(initial_x=x_coordinates[n], initial_y=y_coordinates[n], species=self.species_name, index=n, separation_constant=self.separation)
            individual.group = self.group
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
