import pygame
from pyuilite.uielement import UIElement
from pyuilite.button import TextButton
from pyuilite.constants import *
from pyuilite.config import FONT
from pyuilite.root import Root

class Container(UIElement):
    def __init__(self, 
                 position: tuple[int, int] = (0,0),
                 position_centered: tuple[int, int] = None,
                 font: str = FONT,
                 fontsize: int = 20, 
                 font_color: pygame.Color = pygame.Color("#ebdbb2"),
                 bg_color: pygame.Color = pygame.Color("#282828"),
                 padding: int = 10,
                 gap: int = 10,
                 border_radius: int = 0,
                 on_click = None,
                 direction: str = COLUMN,
                 abs_width: int = None,
                 abs_height: int = None,
                 background: bool = True,
                 children: list[UIElement] = [],
                 float: str = "left",
                 absolute: bool = False,
                 minimize: bool = True) -> None:
        super().__init__(
                         "",
                         position, 
                         position_centered,
                         font,
                         fontsize,
                         font_color,
                         bg_color,
                         padding,
                         border_radius,
                         on_click,
                         background,
                         float,
                         absolute)
        
        # container-specific properties
        self.gap = gap
        self.direction = direction
        self.abs_width = abs_width
        self.abs_height = abs_height

        self.children: list[UIElement] = children
        # change children's parental status
        for child in self.children:
            child.parent = self

        self.position = position
        if position_centered:
            self.position = (position_centered[0] - (width//2),
                             position_centered[1] - (height//2))
        # integrate children
        self.rect = pygame.Rect(self.position[0],
                                self.position[1],
                                10, 10)
        
        # absolute size overriding
        if self.abs_width:
            if self.abs_width == FILL:
                if self.parent:
                    self.abs_width = self.parent.rect.width - (self.padding*2)
                else:
                    self.abs_width = Root.rect.width - (self.padding*2)
        if self.abs_height:
            if self.abs_height == FILL:
                if self.parent:
                    self.abs_height = self.parent.rect.height - (self.padding*2)
                else:
                    self.abs_height = Root.rect.height - (self.padding*2)
        # property
        self.can_minimize = minimize
        if self.can_minimize:
            self.menu_bar: list[UIElement] = []
            self.menu_bar.append(TextButton(text="X", 
                                            fontsize=25,
                                            bg_color=pygame.Color("red"), 
                                            font_color=pygame.Color("#282828"),
                                            on_click=self.kill,
                                            padding=2
                                            ))
            self.menu_bar.append(TextButton(text="-", 
                                            fontsize=25,
                                            bg_color=pygame.Color("yellow"), 
                                            font_color=pygame.Color("#282828"),
                                            on_click=self.toggle_minimize,
                                            padding=2
                                            ))
        

        width, height = self.update_changes()
        
        self.rect = pygame.Rect(self.position[0], self.position[1], width, height)
        

        # states
        self.minimized = False
    def toggle_minimize(self):
        self.minimized = not self.minimized
    def get_max_width(self) -> int:
        m = 0
        for child in self.children:
            if child.rect.width > m:
                m = child.rect.width
        return m
    def get_max_height(self) -> int:
        m = 0
        for child in self.children:
            if child.rect.height > m:
                m = child.rect.height
        return m
    def update(self, target_pos: tuple[int, int], events: list[pygame.event.Event]):
        if self.rect.topleft != self.position:
            
            for child in self.children:
                child.rect.x += (self.rect.x - self.position[0])
                child.rect.y += (self.rect.y - self.position[1])

            self.position = self.rect.topleft

        self.update_children(target_pos, events)
        if self.can_minimize:
            for item in self.menu_bar:
                item.update(target_pos, events)
    def update_changes(self) -> [int, int]:
        width = self.padding*2
        height = self.padding*2
        if self.can_minimize:
            height += 50

        position = self.position
        padding = self.padding

        if self.direction == "column":
            width += self.get_max_width()
            if self.abs_width:
                width = self.abs_width
            for child in self.children:
                if not child.absolute:
                    if child.float == LEFT:
                        child.rect.x = position[0] + padding
                    elif child.float == RIGHT:
                        child.rect.right = position[0] + width - padding
                    elif child.float == CENTER:
                        child.rect.centerx = position[0] + (width/2)
                    child.rect.y = height + position[1] - padding
                    
                    height += child.rect.height + self.gap
                    child.update_changes()
            height -= self.gap
                
        elif self.direction == "row":
            height += self.get_max_height()
            if self.abs_height:
                height = self.abs_height
            for child in self.children:
                if not child.absolute:
                    if child.float == LEFT:
                        child.rect.y = position[1] + padding
                    elif child.float == RIGHT:
                        child.rect.bottom = position[1] + height - self.padding
                    elif child.float == CENTER:
                        child.rect.centery = position[1] + (height / 2)
                    child.rect.x = width + position[0] - padding
                    width += child.rect.width + self.gap
                    child.update_changes()
            width -= self.gap
        
        if self.abs_width:
            width = self.abs_width
        if self.abs_height:
            height = self.abs_height

        self.rect.width = width
        self.rect.height = height

        # update menu bar
        if self.can_minimize:
            bar_width = 0
            for index, item in enumerate(self.menu_bar):
                item.rect.right = self.rect.right - bar_width
                item.rect.y = self.rect.y
                bar_width += item.rect.width
       

        return [width, height]
    def draw(self, surface):
        if not self.minimized:
            if self.background:
                pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=self.border_radius)
            self.draw_children(surface)
        else:
            if self.background:
                pygame.draw.rect(surface, self.bg_color, pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.menu_bar[0].rect.height), border_radius=self.border_radius)
        if self.can_minimize:
            for item in self.menu_bar:
                item.draw(surface)
    def draw_children(self, surface: pygame.Surface):
        for child in self.children:
            child.draw(surface)
    def update_children(self, target_pos: tuple[int, int], events: list[pygame.event.Event]):
        for child in self.children:
            child.update(target_pos, events)
    def add_child(self, child: UIElement):
        self.children.append(child)
        child.parent = self
    def insert_child(self, index, child: UIElement):
        self.children.insert(index, child)
        child.parent = self
    def minimize(self):
        pass
    def draw_menu_bar(self):
        pass
    def add_menu_bar_item(self, child):
        pass