from com.davrodrila.chipy8.Memory.Memory import Memory


class CPU:

    GENERAL_PURPOSE_REGISTER_SIZE = 0xFF
    I_REGISTER_SIZE = 0xFFFF
    PROGRAM_COUNTER_SIZE = 0xFFFF
    STACK_POINTER_SIZE = 0xFF
    STACK_SIZE = 0xF
    STACK_ADDRESS_SIZE = 0xFFFF

    def __init__(self):

        self.memory = Memory()

        #General Purpose 8 bit registers

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

        # 16 bit register used to store addresses. Only the least significant 12 bits are used
        self.I = self.I_REGISTER_SIZE

        # Currently executing memory address
        self.program_counter = self.PROGRAM_COUNTER_SIZE

        # Point to the top level of the stack
        self.stack_pointer = self.STACK_POINTER_SIZE

        # Initialize stack array
        self.stack = [self.STACK_ADDRESS_SIZE for i in range(self.STACK_SIZE)]



