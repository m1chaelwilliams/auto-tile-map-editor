import pygame
from pyuilite.config import *

class UIElement:
    def __init__(self, 
                 text: str = "", 
                 position: tuple[int, int] = (0,0),
                 position_centered: tuple[int, int] = None,
                 font: str = FONT,
                 fontsize: int = 20, 
                 font_color: pygame.Color = pygame.Color("#ebdbb2"),
                 bg_color: pygame.Color = pygame.Color("#3c3836"),
                 padding: int = 10,
                 border_radius: int = 0,
                 on_click = None,
                 background: bool = True,
                 float: str = "left",
                 absolute: bool = False) -> None:
        self.value = str(text)
        self.font = font
        self.fontsize = fontsize
        self.font_color = font_color
        self.bg_color = bg_color
        self.hover_color = self.gen_hover_color(self.bg_color)
        self.padding = padding
        self.border_radius = border_radius
        self.on_click = on_click
        self.position = position
        self.position_centered = position_centered
        self.background = background
        self.float = float
        self.absolute = absolute

        self.rect: pygame.Rect = None
        self.surface: pygame.Surface = None
        self.parent: UIElement = None
        self.children: list[UIElement] = []
    def update(self, *args, **kwargs):
        pass
    def update_changes(self):
        pass
    def draw(self, *args, **kwargs):
        pass
    def kill(self):
        if self.parent:
            self.parent.children.remove(self)
            self.parent.update_changes()

    # utils
    def gen_hover_color(self, color: pygame.Color) -> pygame.Color:
        r = color.r + 20
        if r > 255:
            r = 255
        g = color.g + 20
        if g > 255:
            g = 255
        b = color.b + 20
        if b > 255:
            b = 255
        return pygame.Color(r,g,b)