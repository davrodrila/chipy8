import pygame
from pygame.locals import *
from pygame import Color

CHIP_8_HEIGHT = 32

CHIP_8_WIDTH = 64

NO_SCALE = 1

BASE_DRAWING_SCALE = 1


class Screen:
    def __init__(self, scale_factor):
        self.screen_width = CHIP_8_WIDTH+1
        self.screen_height = CHIP_8_HEIGHT+1

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
        for x in range(self.screen_width):
            for y in range(self.screen_height):
                self.draw_at_screen_position(x, y, self.screen_data[x][y])
        pygame.display.update()

    def draw_at_screen_position(self, x, y, draw_color):
        pygame.draw.rect(self.screen_surface, draw_color, (
            x * self.scale_factor, y * self.scale_factor, BASE_DRAWING_SCALE * self.scale_factor,
            BASE_DRAWING_SCALE * self.scale_factor))

    def clear_display(self):
        for x in range(self.screen_width):
            for y in range(self.screen_height):
                self.screen_data[x][y] = self.background_color

    def draw_sprite(self, memory, starting_address, x, y, sprite_size):
        vf = 0
        address = starting_address
        for i in range(0, sprite_size):

            byte = bin(memory.read_from_address(address).byte).format('b')
            byte = byte[2:]
            offset_x = x
            for j in range(0, len(byte)):
                try:
                    if byte[j] == '1':
                    # If this is correct, then the pixel is turned on already. It needs to be turned off and the VF registers should be put to 1

                        if self.screen_data[offset_x][y] == self.drawing_color:
                            self.screen_data[offset_x][y] = self.background_color
                            vf = 1
                        else:
                            self.screen_data[offset_x][y] = self.drawing_color
                    else:
                       self.screen_data[offset_x][y] = self.background_color
                except IndexError:
                    print("Error accessing X:%s Y:%s " % (x, y))
                offset_x += 1

            address += 1
            y += 1
        return vf
