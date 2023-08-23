import pygame
from basescene import BaseScene
from pyuilite import *
from pyuilite.constants import *
from utils import EventHandler
from statemanager import StateManager

class SettingsMenu(BaseScene):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.view = Container(children=[
            TextButton("< Back", on_click=lambda: self.go_to(StateManager.prev_state))
        ],
        abs_width=self.screen.get_width(),
        abs_height=self.screen.get_height(),
        minimize=False
        )
    def update(self):
        self.view.update(pygame.mouse.get_pos(), EventHandler.events)
    def go_to(self, location: str):
        StateManager.state = location
    def draw(self):
        self.screen.fill("pink")
        self.view.draw(self.screen)