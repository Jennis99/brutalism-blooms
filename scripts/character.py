import pygame as pg
from .settings import TILE_SIZE, CHARACTER_SPEED
import math


class Character:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y

        self.render_x = 0
        self.render_y = 0

        # Animation setup
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_delay = 100  # Milliseconds between frames
        self.facing_direction = 'down'
        self.is_moving = False

        # Load sprite sheet and set up animations
        self.move_sheet = pg.image.load("assets/graphics/Char_002.png")
        self.idle_sheet = pg.image.load("assets/graphics/Char_002_Idle.png")
        self.animations = {
            'down': [],
            'up': [],
            'left': [],
            'right': [],
            'idle_down': [],
            'idle_up': [],
            'idle_left': [],
            'idle_right': []
        }
        # Sprite sheet piece size
        self.frame_width = 72
        self.frame_height = 72

        self.load_animations()

        # Set initial image
        self.image = self.animations['idle_down'][0]
        self.width = self.frame_width
        self.height = self.frame_height

    def load_animations(self):
        # Moving
        for row, direction in enumerate(['down', 'left', 'right', 'up']):
            self.animations[direction] = []
            for frame in range(4):
                frame_surface = pg.Surface((self.frame_width, self.frame_height), pg.SRCALPHA)
                frame_surface.blit(self.move_sheet,
                                   (0, 0),
                                   (frame * self.frame_width, row * self.frame_height, self.frame_width, self.frame_height))
                self.animations[direction].append(frame_surface)
        # Idle
        for row, direction in enumerate(['down', 'left', 'right', 'up']):
            idle_direction = f'idle_{direction}'
            self.animations[idle_direction] = []
            for frame in range(4):
                frame_surface = pg.Surface((self.frame_width, self.frame_height), pg.SRCALPHA)
                frame_surface.blit(self.idle_sheet,
                                   (0, 0),
                                   (frame * self.frame_width, row * self.frame_height, self.frame_width, self.frame_height))
                self.animations[idle_direction].append(frame_surface)

    def update_animation(self, current_time):
        if self.is_moving:
            current_animation = self.facing_direction
        else:
            current_animation = f'idle_{self.facing_direction}'

        if current_time - self.animation_timer > self.animation_delay:
            self.animation_timer = current_time
            self.current_frame = (self.current_frame + 1) % len(self.animations[current_animation])
            self.image = self.animations[current_animation][self.current_frame]

    def move(self, dx, dy, speed):
        if dx != 0 or dy != 0:
            self.is_moving = True

            # Normalize diagonal movement
            if dx != 0 and dy != 0:
                length = math.sqrt(dx * dx + dy * dy)
                dx = dx / length
                dy = dy / length

            # Update facing direction
            if abs(dx) > abs(dy):
                if dx > 0:
                    self.facing_direction = 'right'
                else:
                    self.facing_direction = 'left'
            else:
                if dy < 0:
                    self.facing_direction = 'up'
                else:
                    self.facing_direction = 'down'

            self.grid_x += dx * speed
            self.grid_y += dy * speed
        else:
            self.is_moving = False

    def draw(self, surface, screen_width, screen_height):
        self.render_x = self.grid_x + screen_width / 2 - self.width / 2
        self.render_y = self.grid_y + screen_height / 4 - (self.height - TILE_SIZE)
        surface.blit(self.image, (self.render_x, self.render_y))

    def handle_input(self, keys):
        dx = dy = 0
        if keys[pg.K_UP]:
            dy = -1
        if keys[pg.K_DOWN]:
            dy = 1
        if keys[pg.K_LEFT]:
            dx = -1
        if keys[pg.K_RIGHT]:
            dx = 1

        # Left shift to sprint
        current_speed = CHARACTER_SPEED * 1.5 if keys[pg.K_LSHIFT] else CHARACTER_SPEED
        if keys[pg.K_LSHIFT]:
            current_speed = CHARACTER_SPEED * 1.5
            if self.is_moving:
                self.animation_delay = 75
        else:
            self.animation_delay = 100
            current_speed = CHARACTER_SPEED

        self.move(dx, dy, current_speed)
