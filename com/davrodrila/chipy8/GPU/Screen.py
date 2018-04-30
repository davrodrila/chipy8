import pygame
from pygame.locals import *
from pygame import Color

CHIP_8_HEIGHT = 32

CHIP_8_WIDTH = 64

NO_SCALE = 1

BASE_DRAWING_SCALE = 1


class Screen:

    def __init__(self, scale_factor):
        self.screen_width = CHIP_8_WIDTH
        self.screen_height = CHIP_8_HEIGHT

        if scale_factor <= 0:
            self.scale_factor = NO_SCALE
        else:
            self.scale_factor = scale_factor

        # CHIP8 only emulates either drawing_color or background_color pixels.
        # Here they are defined on RGBA format for PyGame to use

        self.drawing_color = Color(250, 250, 250, 255)
        self.background_color = Color(0, 0, 0, 0)

        self.screen_surface = None
        self.screen_data = [[self.background_color for x in range(self.screen_height)] for y in
                            range(self.screen_width)]

    def init_screen(self):
        pygame.init()
        pygame.display.set_caption("ChiPy8")
        self.screen_surface = pygame.display.set_mode(
            (self.screen_width * self.scale_factor, self.screen_height * self.scale_factor))

    def draw(self):
        self.draw_at_screen_position(10, 10, self.drawing_color)
        for x in range(self.screen_width):
            for y in range(self.screen_height):
                self.draw_at_screen_position(x, y, self.screen_data[x][y])
        pygame.display.update()

    def draw_at_screen_position(self, x, y, draw_color):
        pygame.draw.rect(self.screen_surface, draw_color, (
            x * self.scale_factor, y * self.scale_factor, BASE_DRAWING_SCALE * self.scale_factor,
            BASE_DRAWING_SCALE * self.scale_factor))
