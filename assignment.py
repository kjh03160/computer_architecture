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

class DecodeBinary:

    Opcode = [
    ["R-format", "bltz", "j", "jal", "beq", "bne", "", ""],
    ["addi", "", "slti", "", "andi", "ori", "xori", "lui"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["lb", "", "", "lw", "lbu", "", "", ""],
    ["sb", "", "", "sw", "", "", "", ""]]
    Funct = [
    ["sll", "", "srl", "sra", "", "", "", ""],
    ["jr", "", "", "", "syscall", "", "", ""],
    ["mfhi", "", "mflo", "", "", "", "", ""],
    ["mul", "", "", "", "", "", "", ""],
    ["add", "", "sub", "", "and", "or", "xor", "nor"],
    ["", "", "", "slt", "", "", "", ""]
    ]

    def __init__(self, Simulator):
        self.Simulator = Simulator


    def decode_step(self, inst):
        index = self.Simulator.Index - 1
        inst = inst
        # 바이너리 명령어 해석
        # 해석 결과 값은 딕셔너리로 저장이 좋을 듯
        # result = {'func' : 'add', 'rs' : '0xa', 'rd': ' 0xb', 'rt' : '0xc', 'shamt' : '0'}

        self.Simulator.decode(result)
        ALU.addSubstract(self.Simulator.PC, 4, 0)
        return index

    def decode_All(self, InstMEM):
        for i in InstMEM:
            self.decode_step(i)



class DecodeAssem:
    R_type = ['sll', 'srl', 'sra', 'syscall', 'mfhi', 'mflo', 'mul',
              'add', 'sub', 'and', 'or', 'xor', 'nor', 'slt']
    I_type = ['bltz', 'beq', 'bne', 'addi', 'slti', 'andi', 'ori', 'xori',
              'lui', 'lb', 'lw', 'lbu', 'sb', 'sw']     # rs rt offset
    J_type = ['j', 'jal', 'jr']       # j_ad

    def __init__(self, Simulator):
        self.Simulator = Simulator

    def decode(self, instruction):
        if instruction['func'] == 'syscall':
            sys.exit(0)

        if instruction['func'] in DecodeAssem.R_type:
            x = instruction['rs']
            y = instruction['rd']
            destination = instruction['rt']

            if instruction['shamt'] != 0:       # 시프트 연산
                if instruction['func'] == 'sll':
                    result = ALU.ALU_main(x, y, 0b001)
                    self.Simulator.Regis[destination] = result
                elif instruction['func'] == 'srl':
                    result = ALU.ALU_main(x, y, 0b0010)
                    self.Simulator.Regis[destination] = result
                elif instruction['func'] == 'sra':
                    result = ALU.ALU_main(x, y, 0b0011)
                    self.Simulator.Regis[destination] = result

            else:
                if instruction['func'] == 'add':
                    result = ALU.ALU_main(x, y, 0b1000)
                    self.Simulator.Regis[destination] = result

                elif instruction['func'] == 'sub':
                    result = ALU.ALU_main(x, y, 0b1001)
                    self.Simulator.Regis[destination] = result

                elif instruction['func'] == 'and':
                    result = ALU.ALU_main(x, y, 0b1100)
                    self.Simulator.Regis[destination] = result

                elif instruction['func'] == 'or':
                    result = ALU.ALU_main(x, y, 0b1101)
                    self.Simulator.Regis[destination] = result

                elif instruction['func'] == 'xor':
                    result = ALU.ALU_main(x, y, 0b1110)
                    self.Simulator.Regis[destination] = result

                elif instruction['func'] == 'nor':
                    result = ALU.ALU_main(x, y, 0b1111)
                    self.Simulator.Regis[destination] = result


        elif instruction['func'] in DecodeAssem.I_type:
            rs = instruction['rs']
            destination = instruction['rt']
            offset = instruction['offset']
            if instruction['func'] == 'addi':
                result = ALU.ALU_main(rs, offset, 0b1000)
                self.Simulator.Regis[destination] = result

            elif instruction['func'] == 'subi':
                result = ALU.ALU_main(rs, offset, 0b1001)
                self.Simulator.Regis[destination] = result

            elif instruction['func'] == 'andi':
                result = ALU.ALU_main(rs, offset, 0b1100)
                self.Simulator.Regis[destination] = result

            elif instruction['func'] == 'ori':
                result = ALU.ALU_main(rs, offset, 0b1101)
                self.Simulator.Regis[destination] = result

            elif instruction['func'] == 'xori':
                result = ALU.ALU_main(rs, offset, 0b1110)
                self.Simulator.Regis[destination] = result

            elif instruction['func'] == "beq":
                ALU.ALU_main(rs, destination, 0b1001)
                result = ALU.Z
                if result == 1:
                    self.Simulator.PC += (offset << 2)

            elif instruction['func'] == "bne":
                ALU.ALU_main(rs, destination, 0b1001)
                result = ALU.Z
                if result == 0:
                    self.Simulator.PC  = ALU.ALU_main(self.Simulator.PC, offset << 2, 0b1000)

            elif instruction['func'] == "bltz":
                result = ALU.ALU_main(rs, 0, 0b0100)
                if result == 1:
                    self.Simulator.PC  = ALU.ALU_main(self.Simulator.PC, offset << 2, 0b1000)

            elif instruction['func'] == "slti":
                result = ALU.ALU_main(rs, offset, 0b0100)
                self.Simulator.Regis[destination] = result

            # 'lui', 'lb', 'lw', 'lbu', 'sb', 'sw'

            elif instruction['func'] == "lui":
                self.Simulator.Regis[destination] = offset << 16

            elif instruction['func'] == 'lb': # rt에 rs+offset로부터 byte단위로 데이터로드
                MEM_address = ALU.ALU_main(self.Simulator.Regis[rs], offset << 2, 0b1000)
                pass

            elif instruction['func'] == 'lw':
                MEM_address = ALU.ALU_main(self.Simulator.Regis[rs], offset << 2, 0b1000)
                self.Simulator.Regis[destination] = self.Simulator.DataAccess.MEM_Load(MEM_address)


            elif instruction['func'] == 'lbu':
                MEM_address = ALU.ALU_main(self.Simulator.Regis[destination], offset << 2, 0b1000)
                pass

            elif instruction['func'] == 'sb':
                MEM_address = ALU.ALU_main(self.Simulator.Regis[destination], offset << 2, 0b1000)
                pass

            elif instruction['func'] == 'sw':
                MEM_address = ALU.ALU_main(self.Simulator.Regis[destination], offset << 2, 0b1000)
                value = self.Simulator.Regis[rs]
                self.Simulator.DataAccess.MEM_Store(value, MEM_address)


        else:
            jump_address = instruction['j_add']
            if instruction['func'] == 'j':
                self.Simulator.PC = ALU.ALU_main(((self.Simulator.PC >> 28) << 28), (jump_address << 2), 0b1000)

            elif instruction['func'] == 'jal':
                self.Simulator.Regis[-1] = self.Simulator.PC
                self.Simulator.PC = ALU.ALU_main(((self.Simulator.PC >> 28) << 28), (jump_address << 2), 0b1000)


            elif instruction['func'] == 'jr':
                self.Simulator.PC = self.Simulator.Regis[-1]


class DataAccess:
    def __init__(self, Simulator):
        self.Simulator = Simulator

    def MEM_Load(self, address):
        address -= 0x1000000
        return self.Simulator.DataMEM[address]

    def MEM_Store(self, value, address):
        address -= 0x1000000
        self.Simulator.DataMEM[address] = value




class ALU:
    Z = 0

    @staticmethod
    def ALU_main(x, y, c):
        ret = None
        c32 = (c >> 2) & 0x3
        c10 = c & 0x3
        if c32 == 0:
            ret = ALU.shiftOperation(x, y, c10)

        elif c32 == 1:
            ret = ALU.checkSetless(x, y)

        elif c32 == 2:
            ret = ALU.addSubstract(x, y, c10)
            S = ret
            ALU.Z = ALU.checkZero(S)

        elif c32 == 3:
            ret = ALU.logicOperation(x, y, c10)

        return ret

    @staticmethod
    def EndFunc():
        print("None")

    @staticmethod
    def logicOperation(x, y, c10):
        if c10 < 0 or c10 > 3:
            ALU.EndFunc()

        if c10 == 0:
            return x & y
        elif c10 == 1:
            return x | y
        elif c10 == 2:
            return x ^ y
        elif c10 == 3:
            return ~(x | y)

    @staticmethod
    def shiftOperation(v, y, c):
        ret = None
        v = v & 0x001F # 5bit
        if c < 0 or c > 3:
            ALU.EndFunc()
        if c == 0:
            ret = y
        elif c == 1:
            y = y << v
            ret = y
        elif c == 2:
            y = y >> v
            ret = y
        elif c == 3:
            msb = y
            msb = msb >> 31
            if msb == 1:
                y = y >> v
                y = y | (0xFFFFFFFF << (32 - v))
                ret = y
                return ret
            if msb == 0:
                y = y >> v
                ret = y
                return ret
        return ret

    @staticmethod
    def addSubstract(x, y, c10):
        ret = None
        if c10 < 0x0 or c10 > 0x3:
            print("error")
            ALU.EndFunc()
        elif c10 == 0x0 or c10 == 0x2:
            ret = x + y
        elif c10 == 0x1 or c10 == 0x3:
            ret = x - y

        return ret

    @staticmethod
    def checkZero(s):
        if s == 0:
            return 1
        else:
            return 0

    @staticmethod
    def checkSetless(x, y):
        if x < y:
            return 1
        else:
            return 0

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
