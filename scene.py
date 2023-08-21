import pygame
from tkinter import filedialog
from utils import *
from globals import *
from controller import Controller
from tile import Tile
from cursor import Cursor
from basescene import BaseScene
from statemanager import StateManager
import json
import os

class Scene(BaseScene):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

    def init(self, tileset_file, tilemap_file: str = None):
        self.grid_surface = self.gen_grid((100, 100), spotted=True, clear=CLEAR_GRID, color_1=COLOR_1, color_2=COLOR_2, line_color=LINE_COLOR)
        self.background_surface = pygame.transform.scale(pygame.image.load(BACKGROUND).convert_alpha(), (SCREENWIDTH, SCREENHEIGHT))

        # loading data
        with open(tileset_file, 'r') as f:
            self.data = json.load(f)
        
        self.tilemap_textures = self.load_spritesheets(self.data['SPRITESHEETS'])
        self.tile_textures = self.load_tiles(self.data['TILES'])

        # data structures
        self.layers: list[dict[tuple[int, int], Tile]] = [{}]
        self.layers[0][(0,0)] = Tile(0,0,(0,0))

        # loading tilemap ?
        if tilemap_file:
            self.load_tilemap(tilemap_file)

        self.controller = Controller()
        self.cursor = Cursor(len(self.tile_textures)-1, len(self.tile_textures[0]['variants'])-1)

        # state stuff
        self.active_layer = 0

        # debug
        self.debug_items: dict[str] = {}

        # misc
        self.font = pygame.font.Font(None, 30)
    def update(self) -> None:
        self.controller.update()
        self.cursor.update()
        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()

        position = (mouse_pos[0] - self.controller.position.x)//TILESIZE, (mouse_pos[1] - self.controller.position.y)//TILESIZE
        if mouse[0] and position not in self.layers[self.active_layer]:
            print('clicked!')
            
            self.layers[self.active_layer][position] = Tile(
                self.cursor.active_slot,
                self.cursor.active_variant_index,
                position
            )

            positions_to_check = self.get_surrounding_positions(position)

            for pos in positions_to_check:
                if pos in self.layers[self.active_layer]:
                    variant = 0
                    try:
                        auto_tile_variant = self.get_auto_tile(pos)
                        self.tile_textures[self.layers[self.active_layer][pos].id]['variants'][auto_tile_variant]
                        variant = auto_tile_variant
                    except:
                        variant = 0
                    self.layers[self.active_layer][pos].variant = variant
        if mouse[2] and position in self.layers[self.active_layer]:
            self.layers[self.active_layer].pop(position)

            positions_to_check = self.get_surrounding_positions(position)

            for pos in positions_to_check:
                if pos in self.layers[self.active_layer]:
                    variant = 0
                    try:
                        auto_tile_variant = self.get_auto_tile(pos)
                        self.tile_textures[self.layers[self.active_layer][pos].id]['variants'][auto_tile_variant]
                        variant = auto_tile_variant
                    except:
                        variant = 0
                    self.layers[self.active_layer][pos].variant = variant
        if EventHandler.keydown(pygame.K_PAGEUP):
            self.active_layer += 1
            try:
                self.layers[self.active_layer]
            except:
                self.layers.append({})
        if EventHandler.keydown(pygame.K_PAGEDOWN):
            self.active_layer -= 1
            if self.active_layer < 0:
                self.active_layer = 0
        if EventHandler.scroll_wheel_down():
            self.cursor.variant_count = len(self.tile_textures[self.cursor.active_slot]['variants'])-1
        if EventHandler.scroll_wheel_up():
            self.cursor.variant_count = len(self.tile_textures[self.cursor.active_slot]['variants'])-1
        
        if EventHandler.keydown(pygame.K_e):
            self.export_as_image()
        if EventHandler.keydown(pygame.K_ESCAPE):
            StateManager.state = "pause"

        # debug
        self.debug_items['active_layer'] = f'Active Layer: {self.active_layer}'
        self.debug_items['active_tile_index'] = f'Active Tile Index: {self.cursor.active_slot}'
        self.debug_items['active_variant_index'] = f'Active Variant Index: {self.cursor.active_variant_index}'
        
    def draw(self) -> None:
        self.screen.blit(self.background_surface, (0,0))
        self.screen.blit(self.grid_surface, self.controller.position)
        
        for layer in self.layers:
            for tile in layer.values():
                self.screen.blit(self.tile_textures[tile.id]['variants'][tile.variant], 
                                (tile.position.x + self.controller.position.x,
                                tile.position.y + self.controller.position.y))
   

        mouse_pos = pygame.mouse.get_pos()
        mouse_tile_pos = self.controller.get_tile_pos(mouse_pos)
        self.screen.blit(self.tile_textures[self.cursor.active_slot]['variants'][self.cursor.active_variant_index], 
                         (mouse_tile_pos.x, mouse_tile_pos.y))
        self.draw_tiles()
        self.draw_active_tile()

        # debug
        for index, item in enumerate(self.debug_items.values()):
            surf = self.font.render(item, True, "white", "black")
            self.screen.blit(surf, (10, 10 + (index * 25)))
    def draw_tiles(self):
        x = 0

        for index, tile in enumerate(self.tile_textures):
            self.screen.blit(tile['variants'][0], (x, self.screen.get_height()-100))
            if index == self.cursor.active_slot:
                pygame.draw.rect(self.screen, "white", pygame.Rect(x, 
                                                                   self.screen.get_height()-100, 
                                                                   tile['variants'][0].get_width(), 
                                                                   tile['variants'][0].get_height()), 2)
            x += TILESIZE
    def draw_active_tile(self): # wip
        x = 0
        y = 0

        for index, variant in enumerate(self.tile_textures[self.cursor.active_slot]['variants']):
            if x == 3:
                x = 0
                y += 1
            pos = ((self.screen.get_width()-(TILESIZE*3)) + x*TILESIZE, y*TILESIZE)
            self.screen.blit(variant, pos)
            if index == self.cursor.active_variant_index:
                pygame.draw.rect(self.screen, "white", pygame.Rect(pos[0], pos[1], TILESIZE, TILESIZE), 2)
            x += 1

    # loading assets
    def load_spritesheets(self, tile_data: dict) -> dict[str, pygame.Surface]:
        tilemaps: dict[str, pygame.Surface] = {}
        
        for name, data in tile_data.items():
            tilemaps[name] = pygame.transform.scale(pygame.image.load(data['PATH']).convert_alpha(), 
                                                    (TILESIZE * data['SIZE'][0], 
                                                     TILESIZE * data['SIZE'][1]))
        return tilemaps
    def load_tiles(self, item_data: dict) -> list[dict[str, any]]:
        tiles: list[dict[str, pygame.Surface]] = []

        for name, data in item_data.items():
            variants: list[str, pygame.Surface] = []
            for variant in data['VARIANTS']:
                variant_surf = self.tilemap_textures[data['SOURCE']].subsurface(pygame.Rect(
                    variant['position'][0] * TILESIZE,
                    variant['position'][1] * TILESIZE,
                    variant['size'][0] * TILESIZE,
                    variant['size'][1] * TILESIZE
                ))
                variants.append(variant_surf)
            tiles.append({'name':name, 'variants':variants})
        
        return tiles
    def load_tilemap(self, tilemap_file: str):
        try:
            with open(tilemap_file, 'r') as f:
                data = json.load(f)

            for item in data:
                position = (item['position'][0], item['position'][1])
                id = item['id']
                variant = item['variant']
                self.layers[0][position] = Tile(id, variant, position)
        except:
            pass
    # utils
    def get_auto_tile(self, pos: tuple) -> int:
        up = False
        down = False
        left = False
        right = False

        topleft = False
        topright = False
        bottomleft = False
        bottomright = False

        if self.layers[self.active_layer].get((pos[0], pos[1]-1)):
            up = True
        if self.layers[self.active_layer].get((pos[0], pos[1]+1)):
            down = True
        if self.layers[self.active_layer].get((pos[0]-1, pos[1])):
            left = True
        if self.layers[self.active_layer].get((pos[0]+1, pos[1])):
            right = True
        # corners
        if self.layers[self.active_layer].get((pos[0]-1, pos[1]-1)):
            topleft = True
        if self.layers[self.active_layer].get((pos[0]+1, pos[1]-1)):
            topright = True
        if self.layers[self.active_layer].get((pos[0]-1, pos[1]+1)):
            bottomleft = True
        if self.layers[self.active_layer].get((pos[0]+1, pos[1]+1)):
            bottomright = True

        print(f'bottomleft: {bottomleft}')
        print(f'bottomright: {bottomright}')
        print(f'topleft: {topleft}')
        print(f'topright: {topright}')
            
        num = 0

        if up:
            num += 3
            if not down:
                num += 3
        if left and not right:
            num += 2
        elif left and right:
            num += 1
        
        if not up and not left and not right:
            num = 9

        if num == 4:
            if not bottomleft:
                num = 12
            if not bottomright:
                num = 13
            if not topleft:
                num = 10
            if not topright:
                num = 11
            if not topleft and not topright:
                num = 1
        
        return num


    def gen_grid(self, 
                 size: tuple[int, int], 
                 spotted: bool = True, 
                 clear: bool = False, 
                 color_1: str = "black", 
                 color_2: str = "#282828",
                 line_color: str = "white") -> pygame.Surface:
        surface = pygame.Surface((TILESIZE * size[0], TILESIZE * size[1]))
        
        if spotted:
            for x in range(size[0]):
                for y in range(size[1]):
                    if (x % 2 != 0 and y % 2 == 0) or (x % 2 == 0 and y % 2 != 0):
                        pygame.draw.rect(surface, color_2, pygame.Rect(x*TILESIZE, y*TILESIZE, TILESIZE, TILESIZE))
        if clear:
            surface.set_colorkey((0,0,0,0))
        else:
            surface.fill(color_1)

        for x in range(size[0]):
            pygame.draw.line(surface, line_color, (x*TILESIZE, 0), (x*TILESIZE, size[1] * TILESIZE))
        for y in range(size[1]):
            pygame.draw.line(surface, line_color, (0, y*TILESIZE), (size[0]*TILESIZE, y*TILESIZE))
        
        return surface
    def get_surrounding_positions(self, position: tuple) -> list[tuple[int, int]]:
        return [
            position,
            (position[0]+1, position[1]),
            (position[0]-1, position[1]),
            (position[0], position[1]-1),
            (position[0], position[1]+1),

            (position[0]+1, position[1]+1),
            (position[0]+1, position[1]-1),
            (position[0]-1, position[1]+1),
            (position[0]-1, position[1]-1),
        ]
    # exporting
    def export_as_image(self):
        surf = pygame.Surface((TILESIZE * 100, TILESIZE * 100))
        surf.fill('lightblue')
        for layer in self.layers:
            for tile in layer.values():
                print(f'drawing tile! at {tile.position.x * TILESIZE}, {tile.position.y * TILESIZE}')
                surf.blit(self.tile_textures[tile.id]['variants'][tile.variant], (tile.position.x, tile.position.y))
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")]
        )
        
        pygame.image.save(surf, filepath)
    def export_as_json(self):
        data = []

        for index, layer in enumerate(self.layers):
            for pos, tile in layer.items():
                data.append({'id':tile.id,
                            'name':self.tile_textures[tile.id]['name'],
                            'variant':tile.variant,
                            'position':pos,
                            'layer':index})
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )

        with open(file_path, 'w') as f:
            json.dump(data, f)