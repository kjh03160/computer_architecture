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

        return ret & 0xFFFFFFFF

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
        elif c == 3:
            msb = y
            msb = msb >> 31
            if msb == 1:
                y = y >> v
                y = y | (0xFFFFFFFF << (32 - v))
                ret = y
                return ret & 0xFFFFFFFF
            if msb == 0:
                y = y >> v
                ret = y
                return ret & 0xFFFFFFFF
        elif c == 2:
            y = y >> v
            ret = y

        return ret & 0xFFFFFFFF

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

        return ret & 0xFFFFFFFF

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
