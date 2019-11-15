import struct
import sys
from DataAccess import DataAccess
from DecodeAssem import DecodeAssem
from DecodeBinary import DecodeBinary


class Simulator(DecodeAssem, DecodeBinary, DataAccess):
    def __init__(self, inst = 1000, data = 1000):
        self.InsMEM = [0 for i in range(inst)]   # 주소 : 0x400000
        self.DataMEM = [0 for i in range(data)]  # 주소 : 0x10000000
        self.StackMEM = [2]                      
        self.Regis = [0 for i in range(32)]
        self.Regis[29] = 0x7ffff52c
        self.PC = 0
        self.DecodeAssem = DecodeAssem(self)
        self.DecodeBinary = DecodeBinary(self)
        self.DataAccess = DataAccess(self)

    @classmethod
    def loadProgram(cls, file_name):
        with open(file_name, 'rb') as file:
            inst = struct.unpack('>I', file.read(4))[0]
            data = struct.unpack('>I', file.read(4))[0]
            # print(inst, data)
            simul = cls(inst, data * 4)

            for i in range(inst):
                bin = struct.unpack('>I', file.read(4))[0]
                simul.InsMEM[i] = bin

            for i in range(data):
                value = struct.unpack('>4s', file.read(4))[0]
                simul.DataMEM[i * 4], simul.DataMEM[i * 4 + 1], simul.DataMEM[i * 4 + 2], simul.DataMEM[i * 4 + 3] = value

        pre_inst = [
            0x8fa40000, 0x27a50004,
            0x24a60004, 0x00041080,
            0x00c23021, 0x0c100009,
            0x00000000, 0x3402000a,
            0x0000000c
        ]
        simul.InsMEM = pre_inst + simul.InsMEM
        simul.PC = 0x400000
        return simul


    def step(self):
        if self.PC == 0x400020:
            print("syscall")
            print("All instructions have been executed")
            sys.exit(0)
        print(hex(self.PC))
        Index = (self.PC - 0x400000) // 4
        self.DecodeBinary.decode_step(Index)
        print(hex(self.PC))

    def go(self):
        index = (self.PC - 0x400000) // 4

        for i in range(index, len(self.InsMEM) - 1):
            index = (self.PC - 0x400000) // 4
            self.DecodeBinary.decode_step(index)


    def jump(self, address):
        self.PC = address

    def printMEM(self):
        for i in range(len(self.DataMEM)):
            print("%8X" % self.DataMEM[i])
        print()

    def printRg(self):
        rg_name = ['$0 ', '$at', '$v0', '$v1', '$a0', '$a1', '$a2', '$a3', '$t0', '$t1', '$t2', '$t3', '$t4',
              '$t5', '$t6', '$t7', '$s0', '$s1', '$s2', '$s3', '$s4', '$s5', '$s6', '$s7', '$t8', '$t9',
              '$k0', '$k1', '$gp', '$sp', '$s8', '$ra']
        print_rg = {}
        for i in range(32):
            print_rg[rg_name[i]] = self.Regis[i]

        for rg, val in print_rg.items():
            print("%3s %8X" % (rg, val))
        print()


import sys
s = Simulator()

while True:
    a = input("instruction :").split()
    a = a + ['C:\\Users\\kis03\\Desktop\\자료\\전공\\2학년 2학기\\컴퓨터구조\\과제\\machine_example\\' + a[-1]]
    if a[0] == "l":
        s = s.loadProgram(a[1])
        print("Done")

    elif a[0] == "s":
        s.step()
        print(s.DataMEM)
        s.printRg()

    elif a[0] == 'g':
        s.go()
        s.printRg()

    elif a[0] == "j":
        s.jump(int(a[1]))
    elif a[0] == "m":
        s.printMEM()
    elif a[0] == "r":
        s.printRg()
    elif a[0] == "x":
        sys.exit(0)
    else:
        continue
