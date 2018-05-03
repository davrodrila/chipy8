from com.davrodrila.chipy8.Memory.Memory import Memory
from com.davrodrila.chipy8.GPU.Screen import Screen

class CPU:

    GENERAL_PURPOSE_REGISTERS_LIST = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'}

    GENERAL_PURPOSE_REGISTER_SIZE = 0xFF
    I_REGISTER_SIZE = 0xFFFF
    PROGRAM_COUNTER_SIZE = 0xFFFF
    PROGRAM_COUNTER_ENTRYPOINT = 0x0200
    STACK_POINTER_SIZE = 0xFF
    STACK_SIZE = 0xF
    STACK_ADDRESS_SIZE = 0xFFFF

    def __init__(self, screen, font_directory, font_prefix):

        self.memory = Memory(font_directory, font_prefix)

        # Array containing the 16 general purpose registers of CHIP8.

        self.V = self.initialize_general_registers()

        self.screen = screen

        # 16 bit register used to store addresses. Only the least significant 12 bits are used
        self.I = self.I_REGISTER_SIZE

        # Currently executing memory address
        self.program_counter = self.PROGRAM_COUNTER_ENTRYPOINT

        # Point to the top level of the stack. Right now this doesn't seem correct.
        # Need to look for a way to store stacks. Maybe Python has a Stack built-in?

        self.stack_pointer = self.STACK_POINTER_SIZE

        # Initialize stack array
        self.stack = [self.STACK_ADDRESS_SIZE for i in range(self.STACK_SIZE)]
        # Delay Timer. Substracts 1 at a rate of 60hz, will deactivate when it reaches 0.
        # Not sure what this will be used for yet.
        self.DT = 0
        # Sound timer. Also decrements at a 60hz rate. If the value is greater than 0, sound should play.
        self.ST = 0
        self.map_opcode()

    def initialize_general_registers(self):
        v = []
        for i in self.GENERAL_PURPOSE_REGISTERS_LIST:
            v[self.GENERAL_PURPOSE_REGISTERS_LIST[i]] = self.GENERAL_PURPOSE_REGISTER_SIZE
        return v

    # Lookup table for implementation
    # OPCode list: http://devernay.free.fr/hacks/chip8/C8TECH10.HTM#3.1
    # (Apparently this is isn't 100% accurate but we'll see)

    def map_opcode(self):

        return None

    def do_cycle(self):
        # read opcode from PC
        # Do you always have to load two words or does it depend from the first word byte? Research: ¿1 byte ops?
        first_word = self.memory.read_from_address(self.program_counter)
        self.program_counter +=1
        second_word = self.memory.read_from_address(self.program_counter)

        # execute opcode
        # ¿decrease timers if needed?
        #
        self.screen.draw()
        return None
