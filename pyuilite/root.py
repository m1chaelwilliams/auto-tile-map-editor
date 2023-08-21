import pygame
from pyuilite.uielement import UIElement

class Root:
    '''
    The root the the outermost layer of the UI. This contains all elements
    '''
    rect: pygame.Rect = None
    def __init__(self, x, y, width, height) -> None:
        self.children: list[UIElement] = []
        Root.rect = pygame.Rect(x,y,width, height)
    def add_child(self, child: UIElement):
        self.children.append(child)
        child.parent = self
    def update(self, mouse_pos: tuple[int, int], events: list[pygame.event.Event]):
        for child in self.children:
            child.update(mouse_pos, events)
    def draw(self, surface: pygame.Surface):
        for child in self.children:
            child.draw(surface)
    def kill(self, element: UIElement):
        element.kill()