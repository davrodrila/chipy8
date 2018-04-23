class Memory:

    MEMORY_TOTAL_SIZE = 0xFFF
    PROGRAM_ZONE_START = 0x200
    ETI_660_ZONE_START = 0x600


    def __init__(self):
        self.memory = [0x00 for i in range(self.MEMORY_TOTAL_SIZE)]


    def read_from_address(self, address):
        try:
            return self.memory[address]
        except IndexError:
            return 0x00

    def load_rom_to_memory(self, rom):
        current_rom_pointer = 0
        for i in range(self.PROGRAM_ZONE_START, self.MEMORY_TOTAL_SIZE):
            try:
                self.memory[i] = rom[current_rom_pointer]
            except IndexError:
                break
            current_rom_pointer+=1