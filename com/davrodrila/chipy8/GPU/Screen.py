import pygame
from pygame.locals import *
from pygame import Color

CHIP_8_HEIGHT = 32

CHIP_8_WIDTH = 64

NO_SCALE = 1

BASE_SCALE_TO_DRAW = 1

class Screen:



    def __init__(self, scale_factor):
        self.screen_width = CHIP_8_WIDTH
        self.screen_height = CHIP_8_HEIGHT
        if scale_factor <=0:
            self.scale_factor = NO_SCALE
        else:
            self.scale_factor = scale_factor

        # CHIP8 only emulates either white or black pixels. Here they are defined on RGBA format for pygame to use

        self.white = Color(250, 250, 250, 255)
        self.black = Color(0, 0, 0, 0)

        self.screen_data = [[self.black for x in range(self.screen_height)] for y in range(self.screen_width)]

    def init_screen(self):
        pygame.init()
        pygame.display.set_caption("ChiPy8")
        self.screen_surface = pygame.display.set_mode(
            (self.screen_width * self.scale_factor, self.screen_height * self.scale_factor))
        self.screen_data[10][10] = self.white


    def draw(self):
        self.draw_at_screen_position(10, 10, self.white)
        for x in range(self.screen_width):
             for y in range(self.screen_height):
                 self.draw_at_screen_position(x, y, self.screen_data[x][y])
        pygame.display.update()

    def draw_at_screen_position(self, x, y, color):
        pygame.draw.rect(self.screen_surface, color, (x * self.scale_factor, y * self.scale_factor, BASE_SCALE_TO_DRAW * self.scale_factor, BASE_SCALE_TO_DRAW * self.scale_factor))
