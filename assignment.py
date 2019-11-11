from ALU import ALU
from DataAccess import DataAccess
from DecodeAssem import DecodeAssem
from DecodeBinary import DecodeBinary


class Simulator(DecodeBinary, DecodeAssem, DataAccess):
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
        self.Index = (self.PC - 0x400000) // 4
        self.DecodeBinary = DecodeBinary(self)
        self.DecodeAssem = DecodeAssem(self)
        self.DataAccess = DataAccess(self)

    @classmethod
    def loadProgram(cls, file_name):
        cls.PC = 0x400000
        # 파일 fetch, self.InsMEM에 명령어 담기
        # inst 개수랑 data 개수
        return cls(inst, data)


    def step(self):
        self.DecodeBinary.decode_step(1)

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
while True:
    a = input().split()
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
