from com.davrodrila.chipy8.Memory.Memory import Memory
from com.davrodrila.chipy8.GPU.Screen import Screen

class CPU:

    GENERAL_PURPOSE_REGISTER_SIZE = 0xFF
    I_REGISTER_SIZE = 0xFFFF
    PROGRAM_COUNTER_SIZE = 0xFFFF
    PROGRAM_COUNTER_ENTRYPOINT = 0x0200
    STACK_POINTER_SIZE = 0xFF
    STACK_SIZE = 0xF
    STACK_ADDRESS_SIZE = 0xFFFF

    def __init__(self, screen, font_directory, font_prefix):

        self.memory = Memory(font_directory, font_prefix)

        # General Purpose 8 bit registers. Might have to move those to an array for convenience purposes

        self.V0 = self.GENERAL_PURPOSE_REGISTER_SIZE
        self.V1 = self.GENERAL_PURPOSE_REGISTER_SIZE
        self.V2 = self.GENERAL_PURPOSE_REGISTER_SIZE
        self.V3 = self.GENERAL_PURPOSE_REGISTER_SIZE
        self.V4 = self.GENERAL_PURPOSE_REGISTER_SIZE
        self.V5 = self.GENERAL_PURPOSE_REGISTER_SIZE
        self.V6 = self.GENERAL_PURPOSE_REGISTER_SIZE
        self.V7 = self.GENERAL_PURPOSE_REGISTER_SIZE
        self.V8 = self.GENERAL_PURPOSE_REGISTER_SIZE
        self.V9 = self.GENERAL_PURPOSE_REGISTER_SIZE
        self.VA = self.GENERAL_PURPOSE_REGISTER_SIZE
        self.VB = self.GENERAL_PURPOSE_REGISTER_SIZE
        self.VC = self.GENERAL_PURPOSE_REGISTER_SIZE
        self.VD = self.GENERAL_PURPOSE_REGISTER_SIZE
        self.VE = self.GENERAL_PURPOSE_REGISTER_SIZE
        self.VF = self.GENERAL_PURPOSE_REGISTER_SIZE
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

        self.map_opcode()

    # Lookup table for implementation
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
