from ALU import ALU
from DataAccess import DataAccess
from DecodeAssem import DecodeAssem
from DecodeBinary import DecodeBinary
import struct

class Simulator(DecodeAssem, DecodeBinary, DataAccess):
    def __init__(self, inst = 1000, data = 1000):
        self.InsMEM = [None for i in range(inst)]   # 주소 : 0x400000
        self.DataMEM = [None for i in range(data)]  # 주소 : 0x10000000
        # self.StackMEM = []
        self.Regis = [0 for i in range(32)]
        self.PC = 0
        self.DecodeAssem = DecodeAssem(self)
        self.DecodeBinary = DecodeBinary(self)
        self.DataAccess = DataAccess(self)

    @classmethod
    def loadProgram(cls, file_name):
        with open(file_name, 'rb') as file:
            inst = struct.pack('4B', file.read(1)[0], file.read(1)[0], file.read(1)[0], file.read(1)[0])
            data = struct.pack('4B', file.read(1)[0], file.read(1)[0], file.read(1)[0], file.read(1)[0])
            inst = struct.unpack('>I', inst)[0]
            data = struct.unpack('>I', data)[0]

            simul = cls(inst, data)

            for i in range(inst):
                bin = struct.pack('4B', file.read(1)[0], file.read(1)[0], file.read(1)[0], file.read(1)[0])
                bin = struct.unpack('>I', bin)[0]
                simul.InsMEM[i] = bin

            for i in range(data):
                value = struct.pack('4B', file.read(1)[0], file.read(1)[0], file.read(1)[0], file.read(1)[0])
                value = struct.unpack('>I', value)[0]
                simul.DataMEM[i] = value

        simul.PC = 0x400000
        return simul


    def step(self):
        Index = (self.PC - 0x400000) // 4
        self.DecodeBinary.decode_step(Index)

    def go(self):
        self.DecodeBinary.decode_All(self.InsMEM)

    def jump(self, address):
        self.PC = address

    def printMEM(self):
        for i in range(len(self.DataMEM)):
            print(self.DataMEM[i])
        print()

    def printRg(self):
        rg_name = ['$0', '$at', '$v0', '$v1', '$a0', '$a1', '$a2', '$a3', '$t0', '$t1', '$t2', '$t3', '$t4',
              '$t5', '$t6', '$t7', '$s0', '$s1', '$s2', '$s3', '$s4', '$s5', '$s6', '$s7', '$t8', '$t9',
              '$k0', '$k1', '$gp', '$sp', '$s8', '$ra']
        print_rg = {}
        for i in range(32):
            print_rg[rg_name[i]] = self.Regis[i]

        for rg, val in print_rg.items():
            print(rg, hex(val))
        print()


import sys
s = Simulator()

while True:
    b = [input()]
    a = b + [r'C:\Users\kis03\Desktop\자료\전공\2학년 2학기\컴퓨터구조\과제\machine_example\as_ex01_arith.bin']
    if a[0] == "l":
        s = s.loadProgram(a[1])
    elif a[0] == "s":
        s.step()
    elif a[0] == 'g':
        s.go()
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
