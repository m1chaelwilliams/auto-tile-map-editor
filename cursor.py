import pygame
from utils import EventHandler

class Cursor:
    def __init__(self, tile_count: int, variant_count: int) -> None:
        self.active_slot = 0
        self.active_variant_index = 0
        self.tile_count = tile_count
        self.variant_count = variant_count
    def update(self):
        if EventHandler.keydown(pygame.K_UP):
            self.active_variant_index += 1
            if self.active_variant_index > self.variant_count:
                self.active_variant_index = 0
        if EventHandler.keydown(pygame.K_DOWN):
            self.active_variant_index -= 1
            if self.active_variant_index < 0:
                self.active_variant_index = self.variant_count

        if EventHandler.scroll_wheel_up():
            print('up!')
            self.active_slot += 1
            if self.active_slot > self.tile_count:
                self.active_slot = 0
        if EventHandler.scroll_wheel_down():
            self.active_slot -= 1
            if self.active_slot < 0:
                self.active_slot = self.tile_count