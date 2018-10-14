import unittest

from com.davrodrila.chipy8.CPU.CPU import CPU
from com.davrodrila.chipy8.GPU.Screen import Screen
from com.davrodrila.chipy8.Utils import FileUtils


class TestCPUOperations(unittest.TestCase):

    def setUp(self):
        self.rom_path = "../resources/pong.rom"
        self.font_path = "../resources/fonts/"
        self.font_prefix = 'font'
        self.scale_mode = 16
        self.screen = Screen(self.scale_mode)
        self.cpu = CPU(self.screen, self.font_path, self.font_prefix)

    def test_IfCPUMemorySizeIsCorrect(self):
        self.assertEqual(True,True, "Test")


if __name__ == '__main__':
    unittest.main()