import pygame
from pygame.math import Vector2
from globals import *

class Tile:
    def __init__(self, id: int, variant: int, position: tuple) -> None:
        self.id = id
        self.variant = variant
        self.position = Vector2(position[0] * Globals.TILESIZE, position[1] * Globals.TILESIZE)