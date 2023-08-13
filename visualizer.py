import pygame
import shelve
import sys

class Square(pygame.sprite.Sprite):
    def __init__(self, square_type, width, height, index):
        super().__init__()
        self.square_type = square_type
        if square_type == 'sdr':
            self.color = (10, 12, 14)
        elif square_type == 'input':
            self.color = (15, 22, 7)
        else:
            self.color = (0, 255, 255)
        self.image = pygame.Surface([width, height])
        self.image.fill(self.color)
        self.index = index
        self.rect = pygame.Rect(index[1] * 10, index[0] * 10, 9, 9)

    def update(self, source):
        if self.square_type == 'sdr':
            if self.index in source:
                self.color = (255, 255, 0)
            else:
                self.color = (10, 12, 14)
        elif self.square_type == 'input':
            if self.index in source:
                self.color = (255, 255, 255)
            else:
                self.color = (15, 22, 7)
        else:
            self.color = (0, 255, 255)
        self.image.fill(self.color)
        
class Visualizer:
    def __init__(self, sdr):
        self.save_file = sdr.save_file
        self.sdr = sdr
        self.sdr_width = self.sdr.shape[0] * 10
        self.sdr_height = self.sdr.shape[1] * 10
        self.setup_sdr()
        self.setup_input()

    def setup_screen(self):
        self.screen = pygame.display.set_mode((600, 600))
        self.sdr_win = pygame.Surface((self.sdr_width, self.sdr_height))
        self.input_win = pygame.Surface((self.sdr.input.shape[0] * 10, self.sdr.input.shape[1] * 10))

    def setup_sdr(self):
        self.sdr_group = pygame.sprite.Group()
        for yindex, row in enumerate(self.sdr.columns):
            for xindex, column in enumerate(row):
                self.sdr_group.add(Square('sdr', 9, 9, (yindex, xindex)))
    
    def setup_input(self):
        self.input_group = pygame.sprite.Group()
        for yindex, row in enumerate(self.sdr.input):
            for xindex, column in enumerate(row):
                self.input_group.add(Square('input', 9, 9, (yindex, xindex)))

    def load_state(self):
        f = shelve.open(self.sdr.save_file)
        self.loaded_state = f[str(self.sdr.state_number)]
        f.close()

    def update_sdr(self):
        self.sdr_win.fill((10, 12, 14))
        self.sdr_group.update(self.loaded_state.sdr_state)
        self.sdr_group.draw(self.sdr_win)
    
    def update_input(self):
        self.input_win.fill((15, 22, 7))
        input_sparse =  []
        for yindex, row in enumerate(self.loaded_state.input):
            for xindex, bit in enumerate(row):
                if bit == 1:
                    input_sparse.append((yindex, xindex))
        self.input_group.update(input_sparse)
        self.input_group.draw(self.input_win)

    def update_perms(self):
        pass

    def update_display(self):
        self.update_sdr()
        self.update_input()
        self.screen.blit(self.input_win, (200, 200))
        self.screen.blit(self.sdr_win, (400, 200))
        pygame.display.update()

    def run(self):
        self.load_state()
        self.setup_screen()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            self.update_display()

class SaveManager():
    def __init__(self, save_file):
        self.save_file = save_file
        
    def package_state(self, sdr):
        self.input = sdr.input
        self.sdr_state = [column.index for column in sdr.active_columns]
        self.sdr_perms = {column.index:column.perms for column in sdr.columns.flatten()}
        return(self)