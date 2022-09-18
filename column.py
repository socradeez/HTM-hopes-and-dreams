import random
import numpy as np

class Column:
    def __init__(self, parent, indices, input_indices):
        self.input_shape = parent.input.shape
        self.input_indices = input_indices
        self.indices = indices
        self.inh_radius = parent.inh_radius
        self.perms = {}
        self.boost = 1
        self.parent = parent
    
    def get_new_perms(self):
        #now we assign a random perm value to each input node within the inhibition radius, as calculated above
        for y in range(self.y_floor, self.y_ceil - 1):
            for x in range(self.x_floor, self.x_ceil - 1):
                if (y, x) in self.perms:
                    pass
                else:
                    self.perms[(y, x)] = random.randint(15, 25) / 100

    def get_xy_constraints(self):
        #get y range for perms
        #first we account for y_floor being lower than 0
        if self.input_indices[0] - self.inh_radius < 0:
            self.y_floor = 0
            self.y_ceil = self.input_indices[0] + self.inh_radius + abs(self.input_indices[0] - self.inh_radius)
        #next we account for y_ceil being higher than the highest index of the input
        elif self.input_indices[0] + self.inh_radius > self.input_shape[0] - 1:
            self.y_ceil = self.input_shape[0] - 1
            self.y_floor = self.input_indices[0] - self.inh_radius - ((self.input_indices[0] + self.inh_radius) - self.input_shape[1])
        #next we account for standard cases
        else:
            self.y_floor = self.input_indices[0] - self.inh_radius
            self.y_ceil = self.input_indices[0] + self.inh_radius
        #now do the same for X values. First is the x_floor less than 0
        if self.input_indices[1] - self.inh_radius < 0:
            self.x_floor = 0
            self.x_ceil = self.input_indices[1] + self.inh_radius + abs(self.input_indices[1] - self.inh_radius)
        #next we account for x_ceil being higher than the highest index of the input
        elif self.input_indices[1] + self.inh_radius > self.input_shape[1] - 1:
            self.x_ceil = self.input_shape[1] - 1
            self.x_floor = self.input_indices[1] - self.inh_radius - ((self.input_indices[1] + self.inh_radius) - self.input_shape[1])
        #next we account for standard cases
        else:
            self.x_floor = self.input_indices[1] - self.inh_radius
            self.x_ceil = self.input_indices[1] + self.inh_radius

    def compute_overlap(self):
        input = self.parent.input
        self.overlap = 0
        for input_index in self.perms:
            if input[input_index] == 1 and self.perms[input_index] > 0.2:
                self.overlap += 1
        self.overlap *= self.boost
        if self.overlap > 9:
            print(self.perms)
        return self.overlap

    def learn(self):
        for index in self.perms:
            if self.perms[index] > self.parent.connected_perm:
                self.perms[index] += self.parent.increment_perm
                self.perms[index] = min(1, self.perms[index])
            else:
                self.perms[index] -= self.parent.decrement_perm
                self.perms[index] = max(0, self.perms[index])

    def update_duty_cycle(self):
        pass


        



