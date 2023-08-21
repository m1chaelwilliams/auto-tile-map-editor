import pygame
from pygame.math import Vector2
from globals import *

class Controller:
    def __init__(self) -> None:
        self.position = Vector2()
    def update(self):
        self.input()
    def input(self): # controls are inverted on purpose !
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.position.x += 5
        if keys[pygame.K_d]:
            self.position.x -= 5
        if keys[pygame.K_w]:
            self.position.y += 5
        if keys[pygame.K_s]:
            self.position.y -= 5
    def get_tile_pos(self, position: tuple) -> Vector2:
        pos = ((position[0] - self.position.x), (position[1] - self.position.y))
        return Vector2((pos[0]//TILESIZE)*TILESIZE + self.position.x, 
                       (pos[1]//TILESIZE)*TILESIZE + self.position.y)