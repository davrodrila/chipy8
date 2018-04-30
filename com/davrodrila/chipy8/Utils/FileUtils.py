import mmap

def load_file_from_path(file_path):
    try:
        file = open(file_path, "r+b")
        return mmap.mmap(file.fileno(), 0)
    except ValueError:
        print("Error reading file: %s" % (file_path))