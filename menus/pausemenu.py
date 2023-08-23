import pygame
from basescene import BaseScene
from pyuilite import *
from pyuilite.constants import *
from statemanager import StateManager
from utils import EventHandler
from scene import Scene
import sys

class PauseMenu(BaseScene):
    def __init__(self, screen: pygame.Surface, scene: Scene) -> None:
        super().__init__(screen)

        self.view = Container(
            children=[
                Label("Paused", fontsize=40, float=CENTER),
                TextButton("Export as JSON", on_click=scene.export_as_json, float=CENTER),
                TextButton("Export as PNG", on_click=scene.export_as_image, float=CENTER),
                TextButton("Settings", on_click=lambda: self.go_to("settings"), float=CENTER),
                TextButton("Back To Start", on_click=lambda: self.go_to("start"), float=CENTER),
                TextButton("Quit", on_click=self.quit, float=CENTER)
            ],
            minimize=False,
            abs_width=self.screen.get_width(),
            abs_height=self.screen.get_height(),
            padding=300
        )
    def quit(self):
        pygame.quit()
        sys.exit()
    def go_to(self, loc: str):
        StateManager.set_state(loc)
    def update(self):
        self.view.update(pygame.mouse.get_pos(), EventHandler.events)
        if EventHandler.keydown(pygame.K_ESCAPE):
            StateManager.state = "scene"
    def draw(self):
        self.view.draw(self.screen)
