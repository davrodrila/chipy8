# Appends a Nibble to a byte, to make 12 bits address used by CHIP8.
# The nibble will be the highest order part of the address.
# This is why this bitwise operation sorcery is needed.
from com.davrodrila.chipy8.Utils.Byte import Byte


def concatenate_nibble_before_byte(nibble, byte):
    return (nibble << 8) | (byte & 0x0FF)
