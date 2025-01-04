import pygame as pg
import sys
from .world import World
from .settings import TILE_SIZE
from .utils import draw_text
from .character import Character
from .camera import Camera


class Game:

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        self.camera = Camera(self.width, self.height)
        self.character = Character(5, 5)
        self.world = World(50, 50, self.width, self.height)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

        # Handle character movement input
        keys = pg.key.get_pressed()
        self.character.handle_input(keys)

    def update(self):
        current_time = pg.time.get_ticks()
        self.character.update_animation(current_time)

        self.camera.update(self.character)

    def draw(self):
        # Clear the screen
        self.screen.fill((0, 0, 0))  # Black background

        # Blit the world surface
        self.screen.blit(self.world.world_surface, (self.camera.scroll.x, self.camera.scroll.y))

        for x in range(self.world.grid_length_x):
            for y in range(self.world.grid_length_y):
                render_pos = self.world.world[x][y]["render_pos"]

                tile = self.world.world[x][y]["tile"]
                if tile != "":
                    self.screen.blit(
                        self.world.tiles[tile],
                        (render_pos[0] + self.width / 2 + self.camera.scroll.x,
                         render_pos[1] + self.height / 4 - (self.world.tiles[tile].get_height() - TILE_SIZE) + self.camera.scroll.y)
                    )

        self.character.draw(self.screen, self.width, self.height)

        # FPS Counter
        draw_text(self.screen, f"FPS: {round(self.clock.get_fps())}", 25, (255, 255, 255), (10, 10))

        pg.display.flip()
