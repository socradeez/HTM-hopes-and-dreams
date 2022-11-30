import pygame
import sys
from save import SaveManager
import numpy as np

class SquareSprite(pygame.sprite.Sprite):
    def __init__(self, width, height, index):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.index = index

class InputSprite(SquareSprite):
    def __init__(self, index):
        super().__init__(9, 9, index)
        self.color = (15, 22, 7)
        self.rect = pygame.Rect(index[0] * 10, index[1] * 10, 9, 9)

    def update(self, active_inputs):
        if self.index in active_inputs:
            self.color = (0, 0, 100)
        else:
            self.color = (50, 60, 70)
        self.image.fill(self.color)

class SDRSprite(SquareSprite):
    def __init__(self, index, xoffset):
        super().__init__(9, 9, index)
        self.color = (35, 94, 74)
        self.rect = pygame.Rect(xoffset + index[0] * 10, index[1] * 10, 9, 9)

    def update(self, active_cols):
        if self.index in active_cols:
            self.color = (100, 0, 0)
        else:
            self.color = (35, 94, 74)
        self.image.fill(self.color)

class CursorSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 1, 1)

    def update(self, pos):
        self.rect.update(pos, (1, 1))

class Visualizer:
    def __init__(self, save_file, input_shape, sdr_shape):
        #let's initialize our visualization! Parameter Attributes first!
        self.save_file = save_file
        #next let's designate our load_manager
        self.load_manager = SaveManager('savefile')
        #now let's try loading all the states at once into memory. May fail for larger runs
        self.states = self.load_manager.load_save()
        #get last state from saves
        self.last_state = max([int(x) for x in self.states.keys()])
        self.xoffset = self.states['0'].input.shape[0] * 10
        #and finally we just let it run
        self.run(input_shape, sdr_shape)

    def setup_sdr(self, shape):
        self.sdr_group = pygame.sprite.Group()
        for yindex in range(shape[1]):
            for xindex in range(shape[0]):
                self.sdr_group.add(SDRSprite((yindex, xindex), self.xoffset))

    def setup_input(self, shape):
        self.input_group = pygame.sprite.Group()
        for yindex in range(shape[1]):
            for xindex in range(shape[0]):
                self.input_group.add(InputSprite((yindex, xindex)))

    def update(self, time_step):
        inputs = self.states[str(time_step)].input
        active_inputs = np.where(inputs==1)
        active_inputs = [(active_inputs[0][index], active_inputs[1][index]) for index, _ in enumerate(active_inputs[0])]
        self.input_group.update(active_inputs)
        active_cols = self.states[str(time_step)].active_cols
        self.sdr_group.update(active_cols)
        self.input_group.draw(self.screen)
        self.sdr_group.draw(self.screen)

    def run(self, input_shape, sdr_shape):
        #start by setting up our SDR and Input sprite groups and setting time_step to 0
        time_step = 0
        self.setup_sdr(sdr_shape)
        self.setup_input(input_shape)
        cursor_sprite = CursorSprite()
        #initialize the pygame screen given the two shapes and fill it with black
        self.screen = pygame.display.set_mode(((input_shape[0] * 10 + sdr_shape[0] * 10), (input_shape[1] * 10)))
        
        while True:
            self.screen.fill((0, 0, 0))
            self.update(time_step)
            #input event loop; display update is triggered on timestep move
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_LEFT:
                        if time_step == 0:
                            pass
                        else:
                            time_step -= 1
                            self.update(time_step)
                    if event.key == pygame.K_RIGHT:
                        if time_step == self.last_state:
                            pass
                        else:
                            time_step += 1
                            self.update(time_step)
            mouse_pos = pygame.mouse.get_pos()
            cursor_sprite.update(mouse_pos)

            sdr_sprite = pygame.sprite.spritecollideany(cursor_sprite, self.sdr_group)
            if sdr_sprite:
                for perm in self.states[str(time_step)].perms[sdr_sprite.index]:
                    pygame.draw.line(self.screen, (0, 100, 0), (sdr_sprite.index[0] * 10 + 2 + self.xoffset, sdr_sprite.index[1] * 10 + 2), (perm[0] * 10 + 2, perm[1] * 10 + 2))

                

            pygame.display.flip()
            

            




