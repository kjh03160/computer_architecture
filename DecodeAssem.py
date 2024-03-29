from ALU import ALU
import sys

class DecodeAssem:
    R_type = ['sll', 'srl', 'sra', 'syscall', 'mfhi', 'mflo', 'mul',
              'add', 'addu', 'sub', 'and', 'or', 'xor', 'nor', 'slt']
    I_type = ['bltz', 'beq', 'bne', 'addi', 'addiu', 'slti', 'andi', 'ori', 'xori',
              'lui', 'lb', 'lw', 'lbu', 'sb', 'sw']     # rs rt offset
    J_type = ['j', 'jal', 'jr']       # j_ad

    def __init__(self, Simulator):
        self.Simulator = Simulator

    def decode(self, instruction):
        if instruction['func'] == 'syscall':        # 이건 뭐지?
            pass
            # sys.exit(0)

        if instruction['func'] in DecodeAssem.R_type:
            x = self.Simulator.Regis[instruction['rs']]
            y = self.Simulator.Regis[instruction['rt']]
            destination = instruction['rd']
            shamt = instruction['shamt']

            if instruction['shamt'] != 0:       # 시프트 연산
                if instruction['func'] == 'sll':
                    result = ALU.ALU_main(shamt, y, 0b001)
                    self.Simulator.Regis[destination] = result
                elif instruction['func'] == 'srl':
                    result = ALU.ALU_main(shamt, y, 0b0010)
                    self.Simulator.Regis[destination] = result
                elif instruction['func'] == 'sra':
                    result = ALU.ALU_main(shamt, y, 0b0011)
                    self.Simulator.Regis[destination] = result

            else:
                if instruction['func'] == 'add':
                    result = ALU.ALU_main(x, y, 0b1000)
                    self.Simulator.Regis[destination] = result

                elif instruction['func'] == 'addu':
                    result = ALU.ALU_main(x, y & 0xFFFFFFFF, 0b1000)
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
            rs = self.Simulator.Regis[instruction['rs']]
            data = instruction['rt']
            offset = instruction['offset']
            if instruction['func'] == 'addi':
                result = ALU.ALU_main(rs, offset, 0b1000)
                self.Simulator.Regis[data] = result

            elif instruction['func'] == 'addiu':
                result = ALU.ALU_main(rs & 0xFFFFFFFF, offset, 0b1000)
                self.Simulator.Regis[data] = result

            elif instruction['func'] == 'subi':
                result = ALU.ALU_main(rs, offset, 0b1001)
                self.Simulator.Regis[data] = result

            elif instruction['func'] == 'andi':
                result = ALU.ALU_main(rs, offset, 0b1100)
                self.Simulator.Regis[data] = result

            elif instruction['func'] == 'ori':
                result = ALU.ALU_main(rs, offset, 0b1101)
                self.Simulator.Regis[data] = result

            elif instruction['func'] == 'xori':
                result = ALU.ALU_main(rs, offset, 0b1110)
                self.Simulator.Regis[data] = result

            elif instruction['func'] == "beq":
                ALU.ALU_main(rs, self.Simulator.Regis[data], 0b1001)
                result = ALU.Z
                if result == 1:
                    self.Simulator.PC += ALU.ALU_main(self.Simulator.PC, (offset - 1 << 2), 0b1000)

            elif instruction['func'] == "bne":
                ALU.ALU_main(rs, self.Simulator.Regis[data], 0b1001)
                result = ALU.Z
                if result == 0:
                    self.Simulator.PC  = ALU.ALU_main(self.Simulator.PC, (offset - 1 << 2), 0b1000)

            elif instruction['func'] == "bltz":
                result = ALU.ALU_main(rs, 0, 0b0100)
                if result == 1:
                    self.Simulator.PC  = ALU.ALU_main(self.Simulator.PC, (offset - 1 << 2), 0b1000)

            elif instruction['func'] == "slti":
                result = ALU.ALU_main(rs, offset, 0b0100)
                self.Simulator.Regis[data] = result

            # 'lui', 'lb', 'lw', 'lbu', 'sb', 'sw'

            elif instruction['func'] == "lui":
                self.Simulator.Regis[data] = offset << 16

            elif instruction['func'] == 'lb':
                MEM_address = ALU.ALU_main(self.Simulator.Regis[rs], offset >> 2, 0b1000)
                self.Simulator.Regis[data] = self.Simulator.DataAccess.MEM_LoadByte(MEM_address)

            elif instruction['func'] == 'lw':
                rs = instruction['rs']
                MEM_address = ALU.ALU_main(self.Simulator.Regis[rs], offset >> 2, 0b1000)
                self.Simulator.Regis[data] = self.Simulator.DataAccess.MEM_LoadWord(MEM_address)


            elif instruction['func'] == 'lbu':
                MEM_address = ALU.ALU_main(self.Simulator.Regis[data], offset >> 2, 0b1000)
                self.Simulator.Regis[data] = self.Simulator.DataAccess.MEM_LoadByteU(MEM_address)


            elif instruction['func'] == 'sb':
                rs = instruction['rs']
                MEM_address = ALU.ALU_main(self.Simulator.Regis[rs], offset >> 2, 0b1000)
                value = self.Simulator.Regis[data]
                self.Simulator.DataAccess.MEM_StoreByte(value, MEM_address)

            elif instruction['func'] == 'sw':
                rs = instruction['rs']
                MEM_address = ALU.ALU_main(self.Simulator.Regis[rs], offset >> 2, 0b1000)
                value = self.Simulator.Regis[data]
                self.Simulator.DataAccess.MEM_StoreWord(value, MEM_address)


        else:
            if instruction['func'] == 'j':
                jump_address = instruction['j_add']
                self.Simulator.PC = ALU.ALU_main((self.Simulator.PC & 0xF0000000), (jump_address << 2), 0b1000)

            elif instruction['func'] == 'jal':
                self.Simulator.Regis[-1] = self.Simulator.PC
                jump_address = instruction['j_add']
                self.Simulator.PC = ALU.ALU_main(((self.Simulator.PC >> 28) << 28), (jump_address << 2), 0b1000)


            elif instruction['func'] == 'jr':
                self.Simulator.PC = self.Simulator.Regis[-1]
