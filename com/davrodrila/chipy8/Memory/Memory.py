import com.davrodrila.chipy8.Utils.FileUtils
from com.davrodrila.chipy8.Utils import FileUtils
from com.davrodrila.chipy8.Utils.Byte import Byte


class Memory:
    MEMORY_TOTAL_SIZE = 0xFFF
    PROGRAM_ZONE_START = 0x200
    ETI_660_ZONE_START = 0x600

    # Indicates position specifying the address we should map the sprite to.
    FONT_FILE_STARTING_ADDRESS = 0

    # Where on the font file starts indicating the values for each sprite. Values are expressed on hexadecimal and
    # will later be converted to binary strings when actually drawing the sprites. The sprites are actually specified
    #  in a nibble, but a full byte must be used, padding the least significant nibble with 0's.
    #  In future implementations, the screen will turn on the 1's and leave the 0's turned off.
    # If the pixel it attempts to turn is already turned, it will turn it off.

    FONT_FILE_SPRITE_DATA_START = 1

    # Indicates maximun filesize of the font file used. CHIP8 specs indicate all the fonts of the same size.
    # But I rather have this here as a reminder
    FONT_FILE_SIZE = 6

    # List of the font system built in the CHIP8 system
    BUILTIN_FONT_SPRITE_LIST = {0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF}

    def __init__(self, font_directory, font_prefix):
        self.memory = [0x00 for i in range(self.MEMORY_TOTAL_SIZE)]

        self.font_directory = font_directory
        self.font_prefix = font_prefix
        self.font_starting_addresses = []
        self.load_built_in_sprites()
        print("")

    def read_from_address(self, address) -> Byte:
        try:
            return Byte(self.memory[address])
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
        font = hex(sprite)[2:]
        font_file = self.font_directory + self.font_prefix + "_" + font
        font = FileUtils.load_file_from_path(font_file)
        starting_address = font[self.FONT_FILE_STARTING_ADDRESS]
        sprite_data = []
        self.font_starting_addresses.insert(sprite,starting_address)
        for i in range(self.FONT_FILE_SPRITE_DATA_START, self.FONT_FILE_SIZE):
            sprite_data.append(font[i])
        self.write_sprite_to_memory(starting_address, sprite_data)

    def write_sprite_to_memory(self, starting_address, sprite_data):
        current_address = starting_address
        for i in range(len(sprite_data)):
            self.write_to_memory(current_address, sprite_data[i])
            current_address += 1

    def get_font_starting_address(self, font_desired):
        try:
            return self.font_starting_addresses[font_desired]
        except (IndexError, TypeError):
            print("Error trying to print font: %s" % (hex(font_desired)))
