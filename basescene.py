import pygame

class BaseScene:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
    def update(self):
        pass
    def draw(self):
        pass