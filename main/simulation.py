import numpy as np
import sys

class Individual:
    def __init__(self, initial_x, initial_y, species, index):
        self.x = initial_x
        self.y = initial_y
        self.species = species
        self.index = index
        self.x_velocity = 30
        self.y_velocity = 20
        self.center = [0,0]
        self.separation_velocity = [0,0]
        self.alignment_velocity = 0
        self.coherence_velocity = [0, 0]
        self.bait_velocity = [0,0]
        self.edge_force = [0,0]
        self.edge_force_constant = 1


    def set_species(self, species):
        self.species = species

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
        print("distance: {}".format(distance))
        print("self.species.minimal_distance: {}".format(self.species.minimal_distance))
        if (distance < self.species.minimal_distance):
            distance_x = other_individual.x - self.x
            distance_y = other_individual.y - self.y
            distance_radian = np.arctan2(distance_y, distance_x) + np.pi
            separation_velocity = self.species.minimal_distance - distance
            separation_x = np.cos(distance_radian) * separation_velocity
            separation_y = np.sin(distance_radian) * separation_velocity
            separation = [separation_x, separation_y]
            print("self {}".format([self.x, self.y]))
            print("others {}".format([other_individual.x, other_individual.y]))
            print("separation: {}".format(separation))

        return separation

    def is_visible(self, other_individual):
        distance = self.calculate_distance(other_individual.x, other_individual.y)
        return distance < self.species.vision

    def calculate_cohesion(self):
        other_x = []
        other_y = []
        for i in self.species.group:
            if self.is_visible(i):
                other_x.append(i.x)
                other_y.append(i.y)

        self.center = [np.nan_to_num(np.mean(other_x)), np.nan_to_num(np.mean(other_y))]

    def calculate_separation_velocity(self):
        separation_vectors_x = []
        separation_vectors_y = []
        for i in self.species.group:
            if (i.index != self.index):
                individual_separation = self.calculate_individual_separation(i)
                separation_vectors_x.append(individual_separation[0])
                separation_vectors_y.append(individual_separation[1])

        separation_x = np.nan_to_num(np.mean(separation_vectors_x)) * self.species.separation_constant
        separation_y = np.nan_to_num(np.mean(separation_vectors_y)) * self.species.separation_constant
        self.separation_velocity = [separation_x, separation_y]

    def calculate_alignment_velocity(self):
        aligment_velocities_x = []
        aligment_velocities_y = []
        for i in self.species.group:
            if self.is_visible(i):
                if (i.index != self.index):
                    aligment_velocities_x.append(i.x_velocity)
                    aligment_velocities_y.append(i.y_velocity)

        x_alignment_v = np.nan_to_num(np.mean(aligment_velocities_x)) * self.species.alignment_constant
        y_alignment_v = np.nan_to_num(np.mean(aligment_velocities_y)) * self.species.alignment_constant

        self.alignment_velocity = [x_alignment_v, y_alignment_v]

    def calculate_coherence_velocity(self):
        self.calculate_cohesion()
        self.coherence_velocity = np.array([self.center[0] - self.x, self.center[1] - self.y]) * self.species.cohesion_constant

    def calculate_speed_limit(self):
        speed = np.sqrt(self.x_velocity**2 + self.y_velocity**2)
        if speed>self.species.speed_limit :
            self.x_velocity = (self.x_velocity/speed) * self.species.speed_limit
            self.y_velocity = (self.y_velocity/speed) * self.species.\
                speed_limit

    def calculate_force(self, current, maximum):
        excess = (np.abs(maximum-current))
        if (excess > 0):
            return np.abs(maximum-current) * self.edge_force_constant
        else:
            return 0

    def calculate_edge_force(self):
        edge_force_arr = [0, 0]
        if self.x > self.species.maximum_x:
            edge_force_arr[0] = -1 * self.calculate_force(self.x, self.species.maximum_x)
            print(self.x)
        elif self.x < self.species.minimum_x:
            edge_force_arr[0] = 1 * self.calculate_force(self.x, self.species.minimum_x)
            print(self.x)

        if self.y > self.species.maximum_y:
            edge_force_arr[1] = -1 * self.calculate_force(self.y, self.species.maximum_y)
            print(self.y)
        elif self.y < self.species.minimum_y:
            edge_force_arr[1] = self.calculate_force(self.y, self.species.minimum_y)
            print(self.y)

        self.edge_force = edge_force_arr

    def calculate_bait(self):
        self.bait_velocity = np.array([0 - self.x, 0 - self.y]) * self.species.bait_constant

    def calculate_next_move(self):
        self.calculate_separation_velocity()
        self.calculate_alignment_velocity()
        self.calculate_coherence_velocity()
        self.calculate_edge_force()
        self.calculate_bait()
        self.x_velocity = self.x_velocity + self.separation_velocity[0] + self.alignment_velocity[0] + self.coherence_velocity[0] + self.edge_force[0] + self.bait_velocity[0]
        self.y_velocity = self.y_velocity + self.separation_velocity[1] + self.alignment_velocity[1] + self.coherence_velocity[1] + self.edge_force[1] + self.bait_velocity[1]
        self.calculate_speed_limit()
        print("current ID: {}".format(self.index))
        print("current location x: {}, y:{}".format(self.x, self.y))
        print("calculated velocity x: {}, y:{}".format(self.x_velocity, self.y_velocity))
        print("calculate_separation_velocity {} ".format(self.separation_velocity))
        print("calculate_alignment_velocity {} ".format(self.alignment_velocity))
        print("calculate_coherenece_veolcity {}".format(self.coherence_velocity))
        print("calculate_edge_force {}".format(self.edge_force))

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
        self.vision = sys.maxsize
        self.separation_constant = 1
        self.alignment_constant = 1
        self.cohesion_constant = 1
        self.speed_limit = 30
        self.bait_constant = 0

    def add_population(self, n_of_individual, random_range, velocity_range = [[0,0],[0,0]]):
        x_min = random_range[0][0]
        x_max = random_range[0][1]
        y_min = random_range[1][0]
        y_max = random_range[1][1]
        x_coordinates = np.random.uniform(low=x_min, high=x_max, size=n_of_individual)
        y_coordinates = np.random.uniform(low=y_min, high=y_max, size=n_of_individual)

        v_x_min = velocity_range[0][0]
        v_x_max = velocity_range[0][1]
        v_y_min = velocity_range[1][0]
        v_y_max = velocity_range[1][1]
        for n in range(n_of_individual):
            individual = Individual(initial_x=x_coordinates[n], initial_y=y_coordinates[n], species=self, index=np.random.randint(-sys.maxsize, sys.maxsize))
            individual.x_velocity = np.random.uniform(v_x_min, v_x_max)
            individual.y_velocity = np.random.uniform(v_y_min, v_y_max)
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
