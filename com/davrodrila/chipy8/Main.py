from com.davrodrila.chipy8.CPU.CPU import CPU
from com.davrodrila.chipy8.Utils import FileUtils
from com.davrodrila.chipy8.GPU.Screen import Screen

import keyboard
import pygame
from pygame.locals import *


def Main():

    print("Starting Emulator...")

    rom_path = "resources/pong.rom"
    rom = FileUtils.load_rom_from_path(rom_path)
    scale_mode = 16
    screen = Screen(scale_mode)
    cpu = CPU(screen)
    cpu.memory.load_rom_to_memory(rom)

    emulation_is_running = True
    pygame.init()
    screen.init_screen()
    while emulation_is_running:

        cpu.do_cycle()
        events = pygame.event.get()
        for event in events:
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    emulation_is_running = False
                    print("Closing windows...")



Main()
