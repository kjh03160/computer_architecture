from ALU import ALU
from DataAccess import DataAccess
from DecodeAssem import DecodeAssem
from DecodeBinary import DecodeBinary
import struct

class Simulator(DecodeAssem, DecodeBinary, DataAccess):
    def __init__(self, inst = 1000, data = 1000):
        self.InsMEM = [None for i in range(inst)]   # 주소 : 0x400000
        self.DataMEM = [None for i in range(data)]  # 주소 : 0x1000000
        # self.StackMEM = []
        # self.Regis = {'$0': 0, '$at': 0, '$v0': 0, '$v1': 0,
        #                   '$a0': 0, '$a1': 0, '$a2': 0, '$a3': 0,
        #                   '$t0': 0, '$t1': 0, '$t2': 0, '$t3': 0,
        #                   '$t4': 0, '$t5': 0, '$t6': 0, '$t7': 0,
        #                   '$s0': 0, '$s1': 0, '$s2': 0, '$s3': 0,
        #                   '$s4': 0, '$s5': 0, '$s6': 0, '$s7': 0,
        #                   '$t8': 0, '$t9': 0, '$k0': 0, '$k1': 0,
        #                   '$gp': 0, '$sp': 0, '$s8': 0, '$ra': 0}
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
                # print(simul.DataMEM)

        simul.PC = 0x400000
        return simul


    def step(self):
        Index = (self.PC - 0x400000) // 4
        self.DecodeBinary.decode_step(Index)

    def go(self):
        self.DecodeBinary.decode_All(self.InsMEM)

    def jump(self, address):
        pass

    def printMEM(self):
        pass

    def printRg(self):
        pass


import sys
s = Simulator()
# while True:
    # a =' input().split()
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
