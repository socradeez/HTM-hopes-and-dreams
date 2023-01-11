import pygame,sys
from pygame.math import Vector2 as vec
pygame.init()

# Screen Setup
WIDTH = 500
HEIGHT = 500
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
FPS = 60
CLOCK = pygame.time.Clock()


class Slope:
    def __init__(self,pos,face):
        self.x = pos[0]
        self.y = pos[1]
        self.rect = pygame.Rect(self.x,self.y,100,100)
        self.rect.topleft = pos 
        self.face = face
        self.pos = pos 
        if face == 1:
            self.line = (self.rect.topleft,self.rect.bottomright) 
        else:
            self.line = (self.rect.bottomleft,self.rect.topright)
            
        pygame.draw.line(SCREEN,'blue',self.rect.bottomleft,self.rect.topright,1)
        
    
class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.x = pos[0]
        self.y = pos[1]
        self.pos = pos 
        self.rect = pygame.Rect(self.x,self.y,50,50)
        self.rect.topleft = pos
        # Physics
        self.pos_status = None
        self.gravity = 0.8
        self.canjump = True 
        self.x_speed = 4
        self.y_speed = -16
        self.vel = vec(0,0)
        
    def update(self):
        self.get_status()
        self.get_input()
        self.respawn()
        
    def respawn(self):
        '''
        Respawns player at start
        '''
        if self.rect.top > HEIGHT:
            self.rect.topleft = self.pos 
            
    def get_status(self):
        '''
        Retrieve status of player, based on collisions
        '''
        if self.vel.y < 0 or self.vel.y > self.gravity:
            self.pos_status = 'Air'
        else:
            self.pos_status = 'Ground'
     
    def apply_gravity(self):
        '''
        Apply Gravity To Player, Creating A Feeling Of Downward Force
        '''
        self.vel.y += self.gravity
        self.rect.y += self.vel.y

    def get_input(self):
        '''
        Gets keyboard input from user, then moves player accordingly
        '''
        keys = pygame.key.get_pressed()
        # Right
        if keys[pygame.K_LEFT]:
            player.vel.x = -1
        # Left
        elif keys[pygame.K_RIGHT]:
            player.vel.x = 1
        # Static
        else:
            player.vel.x = 0
        # Jump
        if keys[pygame.K_UP]:
            if player.canjump:
                player.vel.y = 0 
                if player.pos_status == 'Ground':
                    player.vel.y += player.y_speed 
                elif player.pos_status == 'Air':
                    player.vel.y += player.y_speed * 0.8
                player.canjump = False 
        
        
platforms = []
sloped = []

player = Player((100,100))
platforms.append(pygame.Rect(50,300,100,100))
platforms.append(pygame.Rect(150,300,100,100))
platforms.append(pygame.Rect(250,300,100,100))
platforms.append(pygame.Rect(350,300,100,100))
platforms.append(pygame.Rect(350,200,100,100))
sloped.append(Slope((250,200),2))
sloped.append(Slope((50,200),1))

def plat_collide_x():
    '''
    Stops player movement on the X AXIS , if the player rect and platform rect collide
    '''
    player.rect.x += player.vel.x * player.x_speed
    for platform in platforms:
        if platform.colliderect(player.rect):
            # Left
            if player.vel.x < 0:
                player.rect.left = platform.right
            # Right
            elif player.vel.x > 0:
                player.rect.right = platform.left 

def plat_collide_y():
    '''
    Stops player movement on the Y AXIS , if the player rect and platform rect collide
    '''
    player.apply_gravity()
    for platform in platforms:
        if platform.colliderect(player.rect):
            # Down
            if player.vel.y > 0:
                player.rect.bottom = platform.top 
                player.vel.y = 0
                player.canjump = True 
            # Up
            elif player.vel.y < 0:
                player.rect.top = platform.bottom 
                player.vel.y = 0

def slope_collide_x():
    '''
    Stops player movement on the X AXIS , if the player rect and slope rect collide
    '''
    pass 

def slope_collide_y():
    '''
    Stops player movement on the Y AXIS , if the player rect and slope rect collide
    '''
    pass 


# Loop       
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update          
    player.update()
    plat_collide_x()
    plat_collide_y()
    # slope_collide_x()
    # slope_collide_y()
    
    # Render
    SCREEN.fill('black')
    pygame.draw.rect(SCREEN,'green',player.rect,1)
    for platform in platforms:
        pygame.draw.rect(SCREEN,'red',platform,1)
    for slope in sloped:
        pygame.draw.rect(SCREEN,'red',slope.rect,1)
        pygame.draw.line(SCREEN,'blue',slope.line[0],slope.line[1],1)
    
    pygame.display.update()
    CLOCK.tick(FPS)
    
    
    