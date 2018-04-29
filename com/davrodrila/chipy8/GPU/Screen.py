import pygame
from pygame.locals import *
from pygame import Color

class Screen:

    def __init__(self, scale_mode):
        self.screen_width = 64
        self.screen_height = 32
        self.scale_mode = scale_mode
        self.white = Color(250, 250, 250, 255)
        self.black = Color(0, 0, 0, 0)
        self.screen_data = [[self.black for x in range(self.screen_height)] for y in range(self.screen_width)]

    def init_screen(self):
        pygame.init()
        pygame.display.set_caption("ChiPy8")
        self.screen_surface = pygame.display.set_mode(
            (self.screen_width * self.scale_mode, self.screen_height * self.scale_mode))
        self.screen_data[10][10] = self.white

    def draw(self):
        self.draw_at_screen_position(10,10,self.white)
        # for x in range(self.screen_width):
        #     for y in range(self.screen_height):
        #         self.draw_at_screen_position(x, y, self.screen_data[x][y])

    def draw_at_screen_position(self, x, y, color):
        self.screen_surface.fill(color, (x,y), color)
