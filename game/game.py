import pygame as pg
import sys
from .world import World
from .settings import TILE_SIZE
from .utils import draw_text


class Game:

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        self.world = World(10, 10, self.width, self.height)

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

    def update(self):
        pass

    def draw(self):

        # Rendering the surface of the world for whole screen starting at 0,0
        self.screen.blit(self.world.world_surface, (0, 0))

        for x in range(self.world.grid_length_x):
            for y in range(self.world.grid_length_y):

                render_pos = self.world.world[x][y]["render_pos"]
                # self.screen.blit(self.world.tiles["block"], (render_pos[0] + self.width / 2, render_pos[1] + self.height / 4))

                tile = self.world.world[x][y]["tile"]
                if tile != "":
                    # This line renders the trees/rocks but needs to move them up by height of tree or rock and the height of a normal tile
                    self.screen.blit(self.world.tiles[tile],
                                     (render_pos[0] + self.width / 2, render_pos[1] + self.height / 4 - (self.world.tiles[tile].get_height() - TILE_SIZE))
                                     )

                # Red grid for debugging
                polygon = self.world.world[x][y]["iso_poly"]
                polygon = [(x + self.width / 2, y + self.height / 4) for x, y in polygon]
                pg.draw.polygon(self.screen, (255, 0, 0), polygon, 1)

        # FPS Counter
        draw_text(self.screen, f"FPS: {round(self.clock.get_fps())}", 25, (255, 255, 255), (10, 10))

        pg.display.flip()
