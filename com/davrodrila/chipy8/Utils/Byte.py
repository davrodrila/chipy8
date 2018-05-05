class Byte:
    # Supporting class that makes it easier to handle bytes and access high and low nibbles.
    # Opcodes need to read the two nibbles from a byte in order to determine registers.
    def __init__(self, byte):
        self.byte = byte

    def get_high_nibble(self):
        return self.byte >> 4

    def get_low_nibble(self):
        return self.byte & 0x0F
