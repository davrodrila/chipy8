from com.davrodrila.chipy8.Memory.Memory import Memory
from com.davrodrila.chipy8.GPU.Screen import Screen
from com.davrodrila.chipy8.Utils import ByteUtils
from com.davrodrila.chipy8.Utils.Byte import Byte
from random import randint


class CPU:
    GENERAL_PURPOSE_REGISTERS_LIST = {0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF}

    GENERAL_PURPOSE_REGISTER_SIZE = 0x00
    I_REGISTER_SIZE = 0x0000
    PROGRAM_COUNTER_SIZE = 0x0000
    PROGRAM_COUNTER_ENTRYPOINT = 0x0200
    STACK_POINTER_VALUE = 0x00
    STACK_SIZE = 0x10
    STACK_ADDRESS_SIZE = 0x0000

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

        self.stack_pointer = self.STACK_POINTER_VALUE

        # Initialize stack array
        self.stack = [self.STACK_ADDRESS_SIZE for i in range(self.STACK_SIZE)]

        # Delay Timer. Subtracts 1 at a rate of 60hz, will deactivate when it reaches 0.
        # Not sure what this will be used for yet.
        self.DT = 0
        # Sound timer. Also decrements at a 60hz rate. If the value is greater than 0, sound should play.
        self.ST = 0
        self.opcodes = self.map_opcodes()

    def map_opcodes(self):
        opcodes = [self.unsupported_opcode for i in range(0x10)]
        opcodes[0x0] = self.misc_operations
        opcodes[0x1] = self.jump_to_addres
        opcodes[0x2] = self.call_addres
        opcodes[0x3] = self.skip_if_vx_equal_to_byte
        opcodes[0x4] = self.skip_if_vx__not_equal_to_byte
        opcodes[0x5] = self.skip_if_vx__equal_to_vy
        opcodes[0x6] = self.load_vx_from_byte
        opcodes[0x7] = self.add_vx_byte
        opcodes[0x8] = self.registers_operation
        opcodes[0x9] = self.skip_if_vx_not_equal_to_vy
        opcodes[0xA] = self.load_i_from_byte
        opcodes[0xB] = self.jump_to_v0_plus_byte
        opcodes[0xC] = self.random_number_bitwise_and
        opcodes[0xD] = self.draw_sprite_on_vx_vy
        opcodes[0xE] = self.keyboard_operations
        opcodes[0xF] = self.timer_and_fonts_opcodes

        return opcodes

    def initialize_general_registers(self):
        temporal_registers = []
        for i in self.GENERAL_PURPOSE_REGISTERS_LIST:
            temporal_registers.insert(i, self.GENERAL_PURPOSE_REGISTER_SIZE)
        return temporal_registers

    # Lookup table for implementation
    # OPCode list: http://devernay.free.fr/hacks/chip8/C8TECH10.HTM#3.1
    # (Apparently this is isn't 100% accurate but we'll see)

    def unsupported_opcode(self, byte1: Byte, byte2: Byte):
        print("Opcode is not supported yet for byte: %s" % (hex(byte1.byte)))

    def do_cycle(self):
        # read opcode from PC
        # Do you always have to load two words or does it depend from the first word byte? Research: ¿1 byte ops?
        first_word = self.memory.read_from_address(self.program_counter)
        self.program_counter += 1
        second_word = self.memory.read_from_address(self.program_counter)
        self.program_counter += 1
        # execute opcode
        # ¿decrease timers if needed?
        #
        print("Attempting opcode %s%s" % (hex(first_word.byte), hex(second_word.byte)[2:]))
        self.opcodes[first_word.get_high_nibble()](first_word, second_word)
        self.screen.draw()
        self.DT -=1
        self.ST -=1

    def misc_operations(self, byte1: Byte, byte2: Byte):
        if byte2 == 0xE0:
            self.clear_screen()
        elif byte2 == 0xEE:
            self.return_from_subroutine()

    def clear_screen(self):
        self.screen.clear_display()

    # TODO: This needs a proper stack implementation
    def return_from_subroutine(self, byte_1: Byte, byte_2: Byte):
        self.program_counter = self.stack.pop(self.stack_pointer) + 2
        self.stack_pointer = -1

    def jump_to_addres(self, byte_1: Byte, byte_2: Byte):
        self.program_counter = ByteUtils.prefix_nibble_to_byte(byte_1.get_low_nibble(), byte_2.byte)

    def call_addres(self, byte_1: Byte, byte_2: Byte):
        self.stack_pointer += 1
        self.stack.append(self.program_counter)
        self.program_counter = ByteUtils.prefix_nibble_to_byte(byte_1.get_low_nibble(), byte_2.byte)

    def skip_if_vx_equal_to_byte(self, byte_1: Byte, byte_2: Byte):
        if byte_2.byte == self.V[byte_1.get_low_nibble()]:
            self.program_counter += 2

    def skip_if_vx__not_equal_to_byte(self, byte_1: Byte, byte_2: Byte):
        if byte_2.byte != self.V[byte_1.get_low_nibble()]:
            self.program_counter += 2

    def skip_if_vx__equal_to_vy(self, byte_1: Byte, byte_2: Byte):
        if self.V[byte_1.get_low_nibble()] == self.V[byte_2.get_high_nibble()]:
            self.program_counter += 2

    def load_vx_from_byte(self, byte_1: Byte, byte_2: Byte):
        self.V[byte_1.get_low_nibble()] = byte_2.byte

    def add_vx_byte(self, byte_1: Byte, byte_2: Byte):
        result = self.V[byte_1.get_low_nibble()] + byte_2.byte
        # Handle the case of overflowing an 8 bit register.
        if result > 0xFF:
            result = result % 0xFF
        self.V[byte_1.get_low_nibble()] = result

    def registers_operation(self, byte_1: Byte, byte_2: Byte):
        # OPcodes starting with 8 are defined by the last nibble of the two byte opcode
        if byte_2.get_low_nibble() == 0x0:
            self.load_vy_into_vx(byte_1, byte_2)
        elif byte_2.get_low_nibble() == 0x1:
            self.bitwise_or_vx_with_vy(byte_1, byte_2)
        elif byte_2.get_low_nibble() == 0x2:
            self.bitwise_and_vx_with_vy(byte_1, byte_2)
        elif byte_2.get_low_nibble() == 0x3:
            self.bitwise_xor_vx_with_vy(byte_1, byte_2)
        elif byte_2.get_low_nibble() == 0x4:
            self.add_vx_to_vy(byte_1, byte_2)
        elif byte_2.get_low_nibble() == 0x5:
            self.subtract_vx_minus_vy(byte_1, byte_2)
        elif byte_2.get_low_nibble() == 0x6:
            self.shift_right_vx_to_vy(byte_1, byte_2)
        elif byte_2.get_low_nibble() == 0x7:
            self.subtract_vy_minus_vx(byte_1, byte_2)
        elif byte_2.get_low_nibble() == 0xE:
            self.shift_right_vx_to_vy(byte_1, byte_2)

    def load_vy_into_vx(self, byte_1: Byte, byte_2: Byte):
        self.V[byte_1.get_low_nibble()] = self.V[byte_2.get_high_nibble()]

    def bitwise_or_vx_with_vy(self, byte_1: Byte, byte_2: Byte):
        self.V[byte_1.get_low_nibble()] = self.V[byte_1.get_low_nibble()] | self.V[byte_2.get_high_nibble()]

    def bitwise_and_vx_with_vy(self, byte_1: Byte, byte_2: Byte):
        self.V[byte_1.get_low_nibble()] = self.V[byte_1.get_low_nibble()] & self.V[byte_2.get_high_nibble()]

    def bitwise_xor_vx_with_vy(self, byte_1: Byte, byte_2: Byte):
        self.V[byte_1.get_low_nibble()] = self.V[byte_1.get_low_nibble()] ^ self.V[byte_2.get_high_nibble()]

    def add_vx_to_vy(self, byte_1: Byte, byte_2: Byte):
        result = self.V[byte_1.get_low_nibble()] + self.V[byte_2.get_high_nibble()]
        if result > 0xFF:
            self.V[0xF] = 1  # F register is used as a carry one flag. We're setting it up like that.
            self.V[byte_1.get_low_nibble()] = result % 0xFF
        else:
            self.V[0xF] = 0
            self.V[byte_1.get_low_nibble()] = result

    def subtract_vx_minus_vy(self, byte_1: Byte, byte_2: Byte):
        if self.V[byte_1.get_low_nibble()] > self.V[byte_2.get_high_nibble()]:
            self.V[0xF] = 1
        else:
            self.V[0xF] = 0
        self.V[byte_1.get_low_nibble()] -= self.V[byte_2.get_high_nibble()]

    def shift_right_vx_to_vy(self, byte_1: Byte, byte_2: Byte):
        # We need to set VF to 1 if least significant bit of Vx is 1.
        # If VX is an even number, then the least significant bit will be 0.
        # In case of odd number, least significant bit must be 1
        if self.V[byte_1.get_low_nibble()] % 2 == 0:
            self.V[0xF] = 0
        else:
            self.V[0xF] = 1
        self.V[byte_1.get_low_nibble()] = self.V[byte_1.get_low_nibble()] >> 1

    def subtract_vy_minus_vx(self, byte_1: Byte, byte_2: Byte):
        if self.V[byte_2.get_high_nibble()] > self.V[byte_1.get_low_nibble()]:
            self.V[0xF] = 1
        else:
            self.V[0xF] = 0
        self.V[byte_1.get_low_nibble()] = self.V[byte_2.get_high_nibble()] - self.V[byte_1.get_low_nibble()]

    def shift_left_vx_to_vy(self, byte_1: Byte, byte_2: Byte):
        # VF needs to be set to 1 in case most significant number of VX is set to 1.
        if self.V[byte_1.get_low_nibble()] >= 0x80:
            self.V[0xF] = 1
        else:
            self.V[0xF] = 0
        self.V[byte_1.get_low_nibble()] = self.V[byte_1.get_low_nibble()] << 1

    def skip_if_vx_not_equal_to_vy(self, byte_1: Byte, byte_2: Byte):
        if self.V[byte_1.get_low_nibble()] != self.V[byte_2.get_high_nibble()]:
            self.program_counter += 2

    def load_i_from_byte(self, byte_1: Byte, byte_2: Byte):
        self.I = ByteUtils.prefix_nibble_to_byte(byte_1.get_low_nibble(), byte_2.byte)

    def jump_to_v0_plus_byte(self, byte_1: Byte, byte_2: Byte):
        address = ByteUtils.prefix_nibble_to_byte(byte_1.get_low_nibble(), byte_2.byte)
        self.program_counter = (address + self.V[0])

    def random_number_bitwise_and(self, byte_1: Byte, byte_2: Byte):
        random_number = randint(0x00, 0xFF)
        result = random_number & byte_2.byte
        self.V[byte_1.get_low_nibble()] = result

    def draw_sprite_on_vx_vy(self, byte_1: Byte, byte_2: Byte):
        sprite_size = byte_2.get_low_nibble()
        x = self.V[byte_1.get_low_nibble()]
        y = self.V[byte_2.get_high_nibble()]
        self.V[0xF] = self.screen.draw_sprite(self.memory, self.I, x, y, sprite_size)

    def keyboard_operations(self, byte_1, byte_2):
        if byte_2.byte == 0x9E:
            self.skip_if_key_vx_pressed(byte_1, byte_2)
        elif byte_2.byte == 0xA1:
            self.skip_if_key_vx_not_pressed(byte_1, byte_2)

    def skip_if_key_vx_pressed(self, byte_1, byte_2):
        pass

    def skip_if_key_vx_not_pressed(self, byte_1, byte_2):
        pass

    def timer_and_fonts_opcodes(self, byte_1: Byte, byte_2: Byte):
        if byte_2.byte == 0x07:
            self.set_vx_to_dt(byte_1, byte_2)
        elif byte_2.byte == 0x0A:
            self.load_pressed_key_into_vx(byte_1, byte_2)
        elif byte_2.byte == 0x15:
            self.set_dt_to_vx(byte_1, byte_2)
        elif byte_2.byte == 0x18:
            self.set_st_to_vx(byte_1, byte_2)
        elif byte_2.byte == 0x1E:
            self.add_vx_to_i(byte_1, byte_2)
        elif byte_2.byte == 0x29:
            self.load_vx_font_to_i(byte_1, byte_2)
        elif byte_2.byte == 0x33:
            self.load_vx_as_bcd_to_i(byte_1, byte_2)
        elif byte_2.byte == 0x55:
            self.store_v0_to_vx_into_i(byte_1, byte_2)
        elif byte_2.byte == 0x65:
            self.read_v0_to_vx_from_i(byte_1, byte_2)

    def set_vx_to_dt(self, byte_1, byte_2):
        self.V[byte_1.get_low_nibble()] = self.DT

    def load_pressed_key_into_vx(self, byte_1, byte_2):
        pass

    def set_dt_to_vx(self, byte_1, byte_2):
        self.DT = self.V[byte_1.get_low_nibble()]

    def set_st_to_vx(self, byte_1, byte_2):
        self.ST = self.V[byte_1.get_low_nibble()]

    def add_vx_to_i(self, byte_1, byte_2):
        self.I += self.V[byte_1.get_low_nibble()]

    def load_vx_font_to_i(self, byte_1: Byte, byte_2: Byte):
        address = self.memory.get_font_starting_address(self.V[byte_1.get_low_nibble()])
        self.I = address

    def load_vx_as_bcd_to_i(self, byte_1, byte_2):
        pass

    def store_v0_to_vx_into_i(self, byte_1, byte_2):
        pass

    def read_v0_to_vx_from_i(self, byte_1, byte_2):
        pass
