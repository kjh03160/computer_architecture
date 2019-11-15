from ALU import ALU
import ctypes
import struct


class DecodeBinary:
    Opcode_list = [
    ["R-format", "bltz", "j", "jal", "beq", "bne", "", ""],
    ["addi", "addiu", "slti", "", "andi", "ori", "xori", "lui"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["lb", "", "", "lw", "lbu", "", "", ""],
    ["sb", "", "", "sw", "", "", "", ""]]

    Funct_list = [
    ["sll", "", "srl", "sra", "", "", "", ""],
    ["jr", "", "", "", "syscall", "", "", ""],
    ["mfhi", "", "mflo", "", "", "", "", ""],
    ["mul", "", "", "", "", "", "", ""],
    ["add", "addu", "sub", "", "and", "or", "xor", "nor"],
    ["", "", "", "slt", "", "", "", ""]
    ]

    def __init__(self, Simulator):
        self.Simulator = Simulator

    def decode_step(self, index):
        self.Simulator.PC = ALU.addSubstract(self.Simulator.PC, 4, 0)
        inst = self.Simulator.InsMEM[index]
        if inst == 0:
            result = {'func' : 'nop'}
        else:
            opCode = inst >> 26
            opCode_front = opCode >> 3
            opCode_back = opCode & 7
            if opCode == 0:
                funct = inst & 63
                funct_front = funct >> 3
                funct_back = funct & 7
                func = self.Funct_list[funct_front][funct_back]
                rs = (inst >> 21) & 31
                rt = (inst >> 16) & 31
                rd = (inst >> 11) & 31
                sh = (inst >> 6) & 31
                result = {'func': func, 'rs' : rs, 'rt' : rt, 'rd' : rd, 'shamt' : sh}


            else:
                func = self.Opcode_list[opCode_front][opCode_back]

                if 'j' in func:
                    j_add = (inst << 6) >> 6 & 0x3FFFFFF
                    result = {'func' : func, 'j_add' : j_add}
                else:
                    offset = inst & 0xFFFF
                    if func[-1] == 'i':
                        temp = struct.pack('>i', inst)
                        offset = struct.unpack('>1h1h', temp)[1]
                    rs = (inst >> 21) & 31
                    rt = (inst >> 16) & 31
                    result = {'func' : func, 'rs' : rs, 'rt' : rt, 'offset' : offset}


            self.Simulator.DecodeAssem.decode(result)
        print(result)
        return self.Simulator.PC
