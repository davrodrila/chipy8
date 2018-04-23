import mmap

def load_rom_from_path(file_path):
    file = open(file_path, "r+b")
    return mmap.mmap(file.fileno(), 0)