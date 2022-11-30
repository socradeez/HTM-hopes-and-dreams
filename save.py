import shelve
import copy

class SaveObject():
    def __init__(self, time_step, input, active_cols, perms):
        self.time_step = time_step
        self.input = input
        self.active_cols = active_cols
        self.perms = perms

class SaveManager():

    def __init__(self, save_file):
        self.save_file = save_file
        
    def save_state(self, time_step, input, active_cols, perms):
        state_save = SaveObject(time_step, input, active_cols, perms)
        with shelve.open(self.save_file) as f:
            f[str(time_step)] = state_save

    #use this method to load an entire save file. May not be suitable for large save files
    def load_save(self):
        with shelve.open(self.save_file) as f:
            a = copy.deepcopy(f)
            return a

    #use this method to load and return a single state
    '''def load_state(self, time_step):
        with shelve.open(self.save_file) as f:
            self.loaded_state = f[time_step]
            return self.loaded_state'''
