import pygame
from pygame.event import Event

class EventHandler:
    events: list[Event] = []

    @staticmethod
    def poll_events() -> None:
        EventHandler.events = pygame.event.get()
    @staticmethod
    def is_event_type(type: int) -> bool:
        for e in EventHandler.events:
            return e.type == type
        return False
    @staticmethod
    def keydown(key) -> bool:
        for e in EventHandler.events:
            if e.type == pygame.KEYDOWN:
                return e.key == key
        return False
    @staticmethod
    def clicked(button: int = 1):
        for e in EventHandler.events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                return e.button == button
        return False
    @staticmethod
    def mouse_up(button: int = 1):
        for e in EventHandler.events:
            if e.type == pygame.MOUSEBUTTONUP:
                return e.button == button
        return False
    @staticmethod
    def scroll_wheel_up() -> bool:
        for e in EventHandler.events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                return e.button == 4
        return False
    @staticmethod
    def scroll_wheel_down() -> bool:
        for e in EventHandler.events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                return e.button == 5
        return False