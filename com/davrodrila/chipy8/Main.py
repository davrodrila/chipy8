from com.davrodrila.chipy8.CPU.CPU import CPU
from com.davrodrila.chipy8.Utils import FileUtils


def Main():
    print("Starting Emulator...")
    rom_path = "resources/pong.rom"
    debug_mode = True
    rom = FileUtils.load_rom_from_path(rom_path)
    cpu = CPU()
    cpu.memory.load_rom_to_memory(rom)

    print(cpu.memory.read_from_address(0x200))


Main()
