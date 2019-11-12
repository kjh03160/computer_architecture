from ALU import ALU

class DataAccess:
    def __init__(self, Simulator):
        self.Simulator = Simulator

    def MEM_LoadWord(self, address):
        address -= 0x10000000
        return self.Simulator.DataMEM[address]

    def MEM_StoreWord(self, value, address):
        address -= 0x10000000
        self.Simulator.DataMEM[address] = value

    def MEM_LoadByte(self, address):
        address -= 0x10000000
        return self.Simulator.DataMEM[address] & 0xFF

    def MEM_LoadByteU(self, address):
        address -= 0x10000000
        result = self.Simulator.DataMEM[address] << 24
        return ALU.ALU_main(24, result, 0b0010)

    def MEM_StoreByte(self, value, address):
        address -= 0x10000000
        self.Simulator.DataMEM[address] = value & 0xFF

