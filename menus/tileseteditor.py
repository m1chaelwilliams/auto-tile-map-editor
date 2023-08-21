import pygame
from basescene import BaseScene
from pyuilite import *
from pyuilite.constants import *
from utils import EventHandler
from tkinter import simpledialog
import os
import json
from globals import *
from statemanager import StateManager

class TilesetEditor(BaseScene):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.view: Container = Container()

        # loading assets
        self.template_tileset = pygame.transform.scale(
            pygame.image.load('assets/sampletilemap.png').convert_alpha(),
            (TILESIZE*3, TILESIZE*5)
        )

        self.spritesheets: list[SpriteSheet] = []
    def open_tileset(self, tileset: str):
        self.view = Container(children=[
            Container(
                children=[
                    TextButton('< Back', fontsize=20, on_click=self.return_to_start),
                    Label(f'Open Tilset: {tileset}', fontsize=20),
                    TextButton("Save", fontsize=20, on_click=self.save),
                    TextButton("Add New Tile", fontsize=20, on_click=self.add_tile)
                ],
                direction=ROW,
                minimize=False
            )
        ],
        abs_width=self.screen.get_width(),
        abs_height=self.screen.get_height(),
        minimize=False,
        background=False,
        direction=COLUMN)

        if os.path.exists(f'tilesets/{tileset}'):
            with open(f'tilesets/{tileset}', 'r') as f:
                data = json.load(f)

                spritesheets = data['SPRITESHEETS']
                tiles = data['TILES']

                for name, sheet in spritesheets.items():
                    surf = pygame.transform.scale(pygame.image.load(sheet['PATH']).convert_alpha(),
                                                  (sheet['SIZE'][0]*TILESIZE, 
                                                   sheet['SIZE'][1]*TILESIZE))
                    self.spritesheets.append(SpriteSheet(name, sheet['PATH'], sheet['SIZE'], surf, tiles, self.template_tileset))
        self.active_tileset = tileset

        # states
        self.active_sheet = 0
    def add_tile(self):
        tile_name = simpledialog.askstring("Input", "Enter Tile Name")
        self.spritesheets[self.active_sheet].tiles.append(Tile(tile_name,
                                                               [],
                                                               [],
                                                               (300, 300)))
    def save(self):
        data = {}
        spritesheet_data = {}
        for sheet in self.spritesheets:
            spritesheet_data[sheet.name] = {
                'PATH':sheet.path,
                'SIZE':sheet.size
            }
        data['SPRITESHEETS'] = spritesheet_data

        tileset_data = {}
        for sheet in self.spritesheets:
            for tile in sheet.tiles:
                variants = []
                for variant in tile.variants:
                    if not variant.empty:
                        variants.append({'position':variant.spritesheet_position,
                                        'variant':variant.ID,
                                        'size':variant.size})

                tileset_data[tile.name] = {
                    'ID':tile.name,
                    'SOURCE':sheet.name,
                    'VARIANTS':variants
                }
        data['TILES'] = tileset_data

        with open(f'tilesets/{self.active_tileset}', 'w') as f:
            json.dump(data, f, indent=4)
    def return_to_start(self):
        StateManager.state = "start"
    def update(self):
        mouse_pos = pygame.mouse.get_pos()

        self.spritesheets[self.active_sheet].update(mouse_pos)
        self.view.update(pygame.mouse.get_pos(), EventHandler.events)

        for tile in self.spritesheets[self.active_sheet].tiles:
            if tile.rect.collidepoint(mouse_pos):
                tile.hovered = True    
                if EventHandler.clicked():
                    self.spritesheets[self.active_sheet].opened_tile = tile
            else:
                tile.hovered = False

    def draw(self):
        self.screen.fill("#282828")

        self.spritesheets[self.active_sheet].draw_tiles(self.screen)
        self.screen.blit(self.spritesheets[self.active_sheet].surf, self.spritesheets[self.active_sheet].rect)
        if self.spritesheets[self.active_sheet].hovered_tile_rect:
            pygame.draw.rect(self.screen, "white", self.spritesheets[self.active_sheet].hovered_tile_rect, 2)
        if self.spritesheets[self.active_sheet].selected_rect:
            pygame.draw.rect(self.screen, "red", self.spritesheets[self.active_sheet].selected_rect, 4)

        self.view.draw(self.screen)

class SpriteSheet:
    def __init__(self, name: str, path: str, size: tuple[int, int], surf: pygame.Surface, tiles: dict[str, dict], template_tile: pygame.Surface) -> None:
        self.name = name
        self.path = path
        self.size = size
        self.surf = surf
        self.rect = self.surf.get_rect(topleft = (550, 100))
        
        self.tiles: list[Tile] = []
        self.opened_tile: Tile = None
        self.template_tile = template_tile

        # sprite sheet stuff
        self.hovered_tile_rect: pygame.Rect = None
        self.selected_rect: pygame.Rect = None

        initial_offset = (TILESIZE*2, TILESIZE*2)
        x_offset = 0
        y_offset = 0
        for name, data in tiles.items():
            if data['SOURCE'] == self.name:
                variants: list[pygame.Surface] = []
                for variant in data['VARIANTS']:
                    variants.append(self.surf.subsurface(pygame.Rect(variant['position'][0] * TILESIZE,
                                                                     variant['position'][1] * TILESIZE,
                                                                     variant['size'][0]*TILESIZE,
                                                                     variant['size'][1]*TILESIZE)))

                self.tiles.append(Tile(name, 
                                       data['VARIANTS'], 
                                       variants, 
                                       (x_offset*TILESIZE + initial_offset[0], 
                                        y_offset*TILESIZE + initial_offset[1])))
                x_offset += 1
                if x_offset > 5:
                    x_offset = 0
                    y_offset += 1
    def update(self, mouse_pos: tuple[int, int]):
        clicked = EventHandler.clicked()

        if self.opened_tile:
            col = None
            for index, rect in enumerate(self.opened_tile.tile_rects):
                if rect.collidepoint(mouse_pos):
                    col = rect
                    if clicked:
                        self.opened_tile.selected_rect = col
                        self.opened_tile.selected_rect_id = index
            if col:
                self.opened_tile.hovered_rect = col
            else:
                self.opened_tile.hovered_rect = None
                
                
        
        if self.rect.collidepoint(mouse_pos):
            pos = self.get_hovered_tile_pos((mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y))
            if clicked:
                if self.opened_tile.selected_rect:
                    self.opened_tile.set_tile(pos, self.surf.subsurface(pygame.Rect(pos[0], pos[1], TILESIZE, TILESIZE)))
            self.hovered_tile_rect = pygame.Rect(pos[0] + self.rect.x, pos[1] + self.rect.y, TILESIZE, TILESIZE)

        
    def get_hovered_tile_pos(self, pos: tuple[int, int]) -> tuple[int, int]:
        return ((pos[0] // TILESIZE) * TILESIZE, (pos[1] // TILESIZE) * TILESIZE)
    def draw_tiles(self, surface: pygame.Surface):
        for tile in self.tiles:
            surface.blit(tile.image, tile.rect)
            if tile.hovered:
                pygame.draw.rect(surface, "white", tile.rect, 2)
        if self.opened_tile:
            surface.blit(self.template_tile, (TILESIZE*2, TILESIZE*6))
            self.opened_tile.draw_tile_set(surface)

class Tile:
    def __init__(self, name: str, variant_data: list, variants: list[pygame.Surface], position: tuple[int, int]) -> None:
        if variants:
            self.image = variants[0]
        else:
            self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft = position)
        self.name = name
        self.hovered = False
        self.variant_images = variants
        self.variant_data = variant_data
        self.variants: list[Variant] = []


        for index in range(15):
            target = -1
            for i, variant in enumerate(self.variant_data):
                if variant['variant'] == index:
                    target = i
            if target != -1:
                position = self.variant_data[target]['position']
                size = self.variant_data[target]['size']

                self.variants.append(Variant(
                    index,
                    (position[0], position[1]),
                    (size[0], size[1]),
                    self.variant_images[target],
                    empty=False
                ))
            else:
                self.variants.append(Variant(
                    0,
                    None
                ))
        

        
        self.tile_rects: list[pygame.Rect] = self.gen_possible_rects()

        self.hovered_rect: pygame.Rect = None
        self.selected_rect: pygame.Rect = None
        self.selected_rect_id: int = None
    def set_tile(self, spritesheet_position: tuple[int, int], image: pygame.Surface):
        # print(f'setting tile as {spritesheet_position}')
        self.variants[self.selected_rect_id].ID = self.selected_rect_id
        self.variants[self.selected_rect_id].image = image
        self.variants[self.selected_rect_id].spritesheet_position = (spritesheet_position[0]/TILESIZE, spritesheet_position[1]/TILESIZE)
        self.variants[self.selected_rect_id].empty = False

        if self.selected_rect_id == 0:
            self.image = image
    def gen_possible_rects(self) -> list[pygame.Rect]:
        rects: list[pygame.Rect] = []

        x = 0
        y = 0
        for index in range (14):
            rects.append(pygame.Rect(x * TILESIZE + (TILESIZE*2), y * TILESIZE + (TILESIZE*6), TILESIZE, TILESIZE))
            x += 1
            if x >= 3:
                x = 0
                y += 1
        return rects
    def draw_tile_set(self, surface: pygame.Surface):
        for variant in self.variants:
            if not variant.empty:
                surface.blit(variant.image, self.tile_rects[variant.ID])
        if self.hovered_rect:
            pygame.draw.rect(surface, "white", self.hovered_rect, 2)
        if self.selected_rect:
            pygame.draw.rect(surface, "red", self.selected_rect, 4)

class Variant:
    def __init__(self, 
                 variant_id: int, 
                 spritesheet_position: tuple[int, int], 
                 size: tuple[int, int] = (1,1),
                 image: pygame.Surface = pygame.Surface((TILESIZE, TILESIZE)),
                 empty: bool = True
                 ) -> None:
        self.ID = variant_id
        self.image = image
        self.size = size
        self.spritesheet_position = spritesheet_position
        self.empty = empty