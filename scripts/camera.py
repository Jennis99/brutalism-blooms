import pygame as pg
from .settings import TILE_SIZE


class Camera:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.scroll = pg.Vector2(0, 0)
        self.speed = 25  # Camera movement speed in pixels

    def update(self, character):
        character_x = character.render_x
        character_y = character.render_y

        # Horizontal scrolling
        if character_x > self.width * 0.97:
            self.scroll.x -= self.speed
            character.grid_x -= self.speed / (TILE_SIZE / 8)  # Adjust to match isometric scaling
        elif character_x < self.width * 0.03:
            self.scroll.x += self.speed
            character.grid_x += self.speed / (TILE_SIZE / 8)

        # Vertical scrolling
        if character_y > self.height * 0.97:
            self.scroll.y -= self.speed
            character.grid_y -= self.speed / (TILE_SIZE / 16)  # Adjust to match isometric scaling
        elif character_y < self.height * 0.03:
            self.scroll.y += self.speed
            character.grid_y += self.speed / (TILE_SIZE / 16)
