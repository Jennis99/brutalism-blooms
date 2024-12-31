import pygame as pg
from .settings import TILE_SIZE, CHARACTER_SPEED


class Character:
    def __init__(self, x, y,):
        self.grid_x = x
        self.grid_y = y
        self.image = pg.image.load("assets/graphics/character.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # Set initial position based on isometric projection
        self.iso_x, self.iso_y = self.grid_x, self.grid_y

    def grid_to_iso(self, grid_x, grid_y):
        iso_x = (grid_x - grid_y) * (TILE_SIZE // 2)
        iso_y = (grid_x + grid_y) * (TILE_SIZE // 4)
        return iso_x, iso_y

    def move(self, dx, dy):
        self.grid_x += dx * CHARACTER_SPEED
        self.grid_y += dy * CHARACTER_SPEED
        self.iso_x, self.iso_y = self.grid_x, self.grid_y  # Modify this to use grid_to_iso if want to move in line with tiles

    def draw(self, surface, screen_width, screen_height):
        render_x = self.iso_x + screen_width / 2 - self.width / 2
        render_y = self.iso_y + screen_height / 4 - (self.height - TILE_SIZE)
        surface.blit(self.image, (render_x, render_y))

    def handle_input(self, keys):
        if keys[pg.K_UP]:
            self.move(0, -1)
        if keys[pg.K_DOWN]:
            self.move(0, 1)
        if keys[pg.K_LEFT]:
            self.move(-1, 0)
        if keys[pg.K_RIGHT]:
            self.move(1, 0)
