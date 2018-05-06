import pygame

from com.davrodrila.chipy8.CPU.CPU import CPU
from com.davrodrila.chipy8.GPU.Screen import Screen
from com.davrodrila.chipy8.Utils import FileUtils
from com.davrodrila.chipy8.Utils.Byte import Byte


def Dissasembler():
    print("Starting Dissasembly...")

    rom_path = "resources/pong.rom"
    font_path = "resources/fonts/"
    font_prefix = 'font'
    rom = FileUtils.load_file_from_path(rom_path)
    scale_mode = 16
    screen = Screen(scale_mode)
    cpu = CPU(screen, font_path, font_prefix)
    cpu.memory.load_rom_to_memory(rom)
    
        



Dissasembler()