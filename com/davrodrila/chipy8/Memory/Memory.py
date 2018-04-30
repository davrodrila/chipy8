import com.davrodrila.chipy8.Utils.FileUtils
from com.davrodrila.chipy8.Utils import FileUtils


class Memory:
    MEMORY_TOTAL_SIZE = 0xFFF
    PROGRAM_ZONE_START = 0x200
    ETI_660_ZONE_START = 0x600
    FONT_FILE_STARTING_ADDRESS = 0
    FONT_FILE_SPRITE_DATA_START = 1
    FONT_FILE_SIZE = 6
    # List of the font system built in the CHIP8 system
    BUILTIN_FONT_SPRITE_LIST = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'}

    def __init__(self, font_directory, font_prefix):
        self.memory = [0x00 for i in range(self.MEMORY_TOTAL_SIZE)]

        self.font_directory = font_directory
        self.font_prefix = font_prefix

        self.load_built_in_sprites()
        print("")

    def read_from_address(self, address):
        try:
            return self.memory[address]
        except IndexError:
            return 0x00

    def write_to_memory(self, address, value):
        self.memory[address] = value

    def load_rom_to_memory(self, rom):
        current_rom_pointer = 0
        for i in range(self.PROGRAM_ZONE_START, self.MEMORY_TOTAL_SIZE):
            try:
                self.memory[i] = rom[current_rom_pointer]
            except IndexError:
                break
            current_rom_pointer += 1

    def load_built_in_sprites(self):
        for sprite in self.BUILTIN_FONT_SPRITE_LIST:
            self.load_sprite_from_file(sprite)

    def load_sprite_from_file(self, sprite):
        font_file = self.font_directory + self.font_prefix + "_" + sprite
        font = FileUtils.load_file_from_path(font_file)
        starting_address = font[self.FONT_FILE_STARTING_ADDRESS]
        sprite_data = []

        for i in range(self.FONT_FILE_SPRITE_DATA_START,self.FONT_FILE_SIZE):
            sprite_data.append(font[i])
        self.write_sprite_to_memory(starting_address, sprite_data)
        return None

    def write_sprite_to_memory(self, starting_address, sprite_data):
        current_address = starting_address
        for i in range(len(sprite_data)):
            self.write_to_memory(current_address, sprite_data[i])
            current_address += 1
