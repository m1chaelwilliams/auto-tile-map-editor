import pygame
from basescene import BaseScene
from pyuilite import *
from pyuilite.constants import *
from statemanager import StateManager
from utils import EventHandler
from tkinter import filedialog
from scene import Scene
from menus.tileseteditor import TilesetEditor
import sys
import json
import os

class StartMenu(BaseScene):
    def __init__(self, screen: pygame.Surface, scene: Scene, tileseteditor: TilesetEditor) -> None:
        super().__init__(screen)
        self.scene = scene
        self.tileseteditor = tileseteditor

        # properties
        self.active_tileset = ""
        self.active_tilemap = ""

        tilesets = os.listdir('tilesets')

        tileset_buttons = []
        for tileset in tilesets:
            tileset_buttons.append(
                Container(children=[
                    TextButton(tileset, on_click=lambda: self.set_tileset(f"tilesets/{tileset}"), float=CENTER),
                    TextButton("Edit", on_click=lambda: self.edit_tileset(tileset), float=CENTER, bg_color=pygame.Color("#458588")),
                ],
                direction=ROW,
                minimize=False)
            )

        tilemap_list = os.listdir('tilemaps')

        tilemap_buttons = []
        for tilemap in tilemap_list:
            tilemap_buttons.append(TextButton(tilemap, on_click=lambda: self.set_tilemap(f"tilemaps/{tilemap}"), float=CENTER))

        left_column = Container(children=[
            Label("Sphere's Tilemap Editor", fontsize=40, float=CENTER),
                TextButton("Start", on_click=self.start, float=CENTER),
                TextButton("Quit", on_click=self.quit, float=CENTER)
        ],
        minimize=False,
        float=CENTER)

        tileset_column = Container(
            children=[
                Label("Tilesets", float=CENTER, fontsize=35, background=False),
                Label("(Select One)", float=CENTER, fontsize=20, background=False, padding=0),
                *tileset_buttons,
                TextButton("Create New", bg_color=pygame.Color("#cc241d"), on_click=self.create_new_tileset, float=CENTER)
            ],
            minimize=False,
            float=CENTER
        )
        tilemap_column = Container(
            children=[
                Label("Tilemaps", float=CENTER, fontsize=35, background=False),
                Label("(Select One)", float=CENTER, fontsize=20, background=False, padding=0),
                *tilemap_buttons,
                TextButton("Create New", bg_color=pygame.Color("#cc241d"), on_click=self.create_new_tilemap, float=CENTER)
            ],
            minimize=False,
            float=CENTER
        )


        self.view = Container(
            children=[
                left_column,
                tilemap_column,
                tileset_column
            ],
            direction=ROW,
            minimize=False,
            abs_width=self.screen.get_width(),
            abs_height=self.screen.get_height(),
            padding=300
        )
    def quit(self):
        pygame.quit()
        sys.exit()
    def start(self):
        if self.active_tilemap and self.active_tileset:
            self.scene.init(self.active_tileset, self.active_tilemap)
            StateManager.state = "scene"
    def set_tileset(self, tileset):
        self.active_tileset = tileset
    def set_tilemap(self, tilemap):
        self.active_tilemap = tilemap
    def create_new_tilemap(self):
        pass
    def create_new_tileset(self):
        pass
    def edit_tileset(self, tileset):
        self.tileseteditor.open_tileset(tileset)
        StateManager.state = "tileseteditor"
    def update(self):
        self.view.update(pygame.mouse.get_pos(), EventHandler.events)
    def draw(self):
        self.view.draw(self.screen)
