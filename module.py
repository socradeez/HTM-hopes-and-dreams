import random
import numpy as np
from column import Column
import shelve
from visualizer import Visualizer, SaveManager

class SDR:
    def __init__(self, shape, input, save_file):
        self.packager = SaveManager(save_file)
        self.save_file = save_file
        self.shape = shape
        self.increment_perm = 0.03
        self.decrement_perm = 0.015
        self.connected_perm = 0.2
        self.inh_radius = 2
        self.active_per_inh_area = 2
        self.input = input
        self.y_ratio = input.shape[0] // shape[0]
        self.x_ratio = input.shape[1] // shape[1]
        self.columns = np.ndarray(shape, dtype=object)
        self.stim_thresh = 2
        self.state_number = 0
        for y_index in range(shape[0]):
            for x_index in range(shape[1]):
                input_indices = (self.y_ratio * y_index, self.x_ratio * x_index)
                self.columns[y_index, x_index] = Column(self, (y_index, x_index), input_indices)
    
    def init_perms(self):
        #vectorize the class methods to make it easy to call them on each instance in self.columns
        vec_get_xy = np.vectorize(Column.get_xy_constraints)
        vec_get_perms = np.vectorize(Column.get_new_perms)
        #call the vectorized function of the method on the entire array
        vec_get_xy(self.columns)
        vec_get_perms(self.columns)

    def get_overlaps(self):
        vec_get_overlap = np.vectorize(Column.compute_overlap)
        self.overlaps = vec_get_overlap(self.columns)

    def get_active_columns(self):
        self.active_columns = []
        for y_index, row in enumerate(self.columns):
            for x_index, column in enumerate(row):
                if y_index - self.inh_radius < 0:
                    y_low = 0
                else:
                    y_low = y_index - self.inh_radius
                if y_index + self.inh_radius > self.columns.shape[0] - 1:
                    y_high = self.columns.shape[0] - 1
                else:
                    y_high = y_index + self.inh_radius
                if x_index - self.inh_radius < 0:
                    x_low = 0
                else:
                    x_low = x_index - self.inh_radius
                if x_index + self.inh_radius > self.columns.shape[1] - 1:
                    x_high = self.columns.shape[1] - 1
                else:
                    x_high = x_index + self.inh_radius
                neighbors = self.columns[y_low:y_high + 1, x_low:x_high + 1]
                flat_neigh = neighbors.flatten()
                flat_neigh = np.array([neighbor.overlap for neighbor in flat_neigh])
                flat_neigh.sort()
                flat_neigh = flat_neigh [::-1]
                min_activity = flat_neigh[self.active_per_inh_area]
                if column.overlap > self.stim_thresh and column.overlap >= min_activity:
                    self.active_columns.append(column)
                    column.active = True
    
    def learn(self):
        for column in self.active_columns:
            column.learn()
    
    def get_adcs(self):
        vec_adc = np.vectorize(Column.update_duty_cycle)
        self.adcs = vec_adc(self.columns)

    def get_boosts(self):
        for y_index, row in enumerate(self.columns):
            for x_index, column in enumerate(row):
                if y_index - self.inh_radius < 0:
                    y_low = 0
                else:
                    y_low = y_index - self.inh_radius
                if y_index + self.inh_radius > self.columns.shape[0] - 1:
                    y_high = self.columns.shape[0] - 1
                else:
                    y_high = y_index + self.inh_radius
                if x_index - self.inh_radius < 0:
                    x_low = 0
                else:
                    x_low = x_index - self.inh_radius
                if x_index + self.inh_radius > self.columns.shape[1] - 1:
                    x_high = self.columns.shape[1] - 1
                else:
                    x_high = x_index + self.inh_radius
                neighbor_adc = self.adcs[y_low:y_high + 1, x_low:x_high + 1]
                column.get_boost(neighbor_adc)
        
    def get_odcs(self):
        pass

    def save_state(self):
        f = shelve.open(self.save_file)
        f[str(self.state_number)] = self.packager.package_state(self)
        f.close()

    def run(self, input):
        self.input = input
        self.init_perms()
        self.get_overlaps()
        self.get_active_columns()
        self.save_state()

ones = np.random.randint(2, size=(10, 10))
test = SDR((5, 5), ones, 'savefile')
test.run(ones)
testviz = Visualizer(test)
testviz.run()


        