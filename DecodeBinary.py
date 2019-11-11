from ALU import ALU


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

