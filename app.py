import pygame
from globals import Globals
import sys
from utils import *
from scene import Scene
from statemanager import StateManager
from basescene import BaseScene
from menus.startmenu import StartMenu
from menus.pausemenu import PauseMenu
from menus.tileseteditor import TilesetEditor
from menus.settingsmenu import SettingsMenu

class App:
    def __init__(self, CONFIG_FILEPATH: str = "config/graphics_config.json") -> None:
        pygame.init()
        Globals.init()

        self.screen = pygame.display.set_mode((Globals.SCREENWIDTH, Globals.SCREENHEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(Globals.TITLE)

        
        self.scene = Scene(self.screen)
        self.tileseteditor = TilesetEditor(self.screen)
        self.settings = SettingsMenu(self.screen)
        self.startmenu = StartMenu(self.screen, self.scene, self.tileseteditor)
        self.pausemenu = PauseMenu(self.screen, self.scene)
        

        StateManager.state = "start"
        self.states: dict[str, BaseScene] = {
            'start':self.startmenu,
            'scene':self.scene,
            'pause':self.pausemenu,
            'settings':self.settings,
            'tileseteditor':self.tileseteditor
        }

    def start(self) -> None:
        

        while self.is_open():
            self.update()
            self.draw()
        self.close()
    def update(self) -> None:
        EventHandler.poll_events()

        self.states[StateManager.state].update()

    def draw(self) -> None:
        self.states[StateManager.state].draw()

        pygame.display.update()
        self.clock.tick(Globals.FPS)
    def is_open(self) -> bool:
        for e in EventHandler.events:
            if e.type == pygame.QUIT:
                return False
        return True
    def close(self) -> None:
        pygame.quit()
        sys.exit()

