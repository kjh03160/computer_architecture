from ALU import ALU


class DecodeBinary:

    Opcode_list = [
    ["R-format", "bltz", "j", "jal", "beq", "bne", "", ""],
    ["addi", "", "slti", "", "andi", "ori", "xori", "lui"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["lb", "", "", "lw", "lbu", "", "", ""],
    ["sb", "", "", "sw", "", "", "", ""]]
    Funct_list = [
    ["sll", "", "srl", "sra", "", "", "", ""],
    ["jr", "", "", "", "syscall", "", "", ""],
    ["mfhi", "", "mflo", "", "", "", "", ""],
    ["mul", "", "", "", "", "", "", ""],
    ["add", "", "sub", "", "and", "or", "xor", "nor"],
    ["", "", "", "slt", "", "", "", ""]
    ]

    def __init__(self, Simulator):
        self.Simulator = Simulator


    def decode_step(self, index):
        self.Simulator.PC = ALU.addSubstract(self.Simulator.PC, 4, 0)
        inst = self.Simulator.InsMEM[index]
        print(hex(inst))
        opCode = inst >> 26
        opCode_front = opCode >> 3
        opCode_back = opCode & 7
        if opCode == 0:
            funct = inst & 63
            funct_front = funct >> 3
            funct_back = funct & 7
            func = self.Opcode_list[funct_front][funct_back]
            rs = (inst >> 21) & 31
            rt = (inst >> 16) & 31
            rd = (inst >> 11) & 31
            sh = (inst >> 6) & 31
            result = {'func': func, 'rs' : rs, 'rt' : rt, 'rd' : rd, 'shamt' : sh}

        else:
            func = self.Opcode_list[opCode_front][opCode_back]
            if 'j' in func:
                j_add = (inst << 6) >> 6
                result = {'func' : func, 'j_add' : j_add}
            else:
                offset = inst & 65535
                rs = (inst >> 21) & 31
                rt = (inst >> 16) & 31
                result = {'func' : func, 'rs' : rs, 'rt' : rt, 'offset' : offset}
        print(result)

        self.Simulator.DecodeAssem.decode(result)
        # return index

    def decode_All(self, InstMEM):
        for i in InstMEM:
            self.decode_step(i)

