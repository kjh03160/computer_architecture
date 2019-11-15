from ALU import ALU

class DataAccess:
    def __init__(self, Simulator):
        self.Simulator = Simulator

    def MEM_LoadWord(self, address):
        if (address & 0xFFF00000) == 0x7FF00000:
            address -= 0x7ffff52c
            index = address // 4
            return self.Simulator.StackMEM.pop()

        address -= 0x10000000
        return self.Simulator.DataMEM[address] & 0xFFFFFFFF

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

    def MEM_StoreWord(self, value, address):
        if (address & 0xFFF00000) == 0x7FF00000:
            address -= 0x7ffff52c
            index = address // 4
            try:
                self.Simulator.StackMEM[index] = value & 0xFFFFFFFF
            except:
                self.Simulator.StackMEM.append(value & 0xFFFFFFFF)
            return
        address -= 0x10000000
        self.Simulator.DataMEM[address] = value & 0xFFFFFFFF

