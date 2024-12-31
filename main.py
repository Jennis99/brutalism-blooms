import pygame as pg
from game.game import Game


def main():

    running = True
    playing = True

    pg.init()
    pg.mixer.init()  # music mixer
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    clock = pg.time.Clock()

    # Menu implementation goes here

    # Game implementation goes here
    game = Game(screen, clock)

    while running:

        # Start menu goes here

        while playing:
            # Game loop goes here
            game.run()


if __name__ == "__main__":
    main()
