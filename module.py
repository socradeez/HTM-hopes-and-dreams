import random
import numpy as np
from column import Column

class Module:
    def __init__(self, shape, input):
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
                
                
                

    

ones = np.ones((6,6))
test = Module((3,3), ones)
test.init_perms()
test.get_overlaps()
test.get_active_columns()

        