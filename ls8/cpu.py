"""CPU functionality."""

import sys

HLT  = 0b00000001
LDI  = 0b10000010
PRN  = 0b01000111
ADD  = 0b10100000
MUL  = 0b10100010
PUSH = 0b01000101
POP  = 0b01000110
CALL = 0b01010000
RET  = 0b00010001

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 0xF4

    def load(self):
        """Load a program into memory."""
        address = 0

        if len(sys.argv) != 2:
            print(f"usage: {sys.argv[0]} filename")
            sys.exit(2)

        try:
            with open(sys.argv[1]) as file:
                for line in file:
                    comment_split = line.split('#')
                    number_string = comment_split[0].strip()

                    if number_string == '':
                        continue

                    instruction = int(number_string, 2)
                    
                    self.ram[address] = instruction
                    address += 1
        
        except FileNotFoundError:
            print(f"{sys.argv[0]}: cound not find {sys.argv[1]}")
            sys.exit(2)

    def ram_read(self, MAR):
        return self.ram[MAR]
    
    def ram_write(self, MAR, MDR):
        self.reg[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        # print(op)

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == MUL:
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def LDI(self):
        MAR = self.ram_read(self.pc + 1)
        MDR = self.ram_read(self.pc + 2)

        self.ram_write(MAR, MDR)

    def PRN(self):
        MAR = self.ram_read(self.pc + 1)

        print(self.reg[MAR])

    def PUSH(self):
        MAR = self.ram_read(self.pc + 1)
        MDR = self.reg[MAR]

        self.sp -= 1
        self.ram[self.sp] = MDR

    def POP(self):
        MDR = self.ram[self.sp]
        MAR = self.ram_read(self.pc + 1)

        self.reg[MAR] = MDR

        if self.sp >= 0xF4:
            print("Underflow Error!")
            sys.exit(1)
        else:
            self.sp += 1

    def CALL(self):
        return_address = self.pc + 2
        self.sp -= 1
        self.ram[self.sp] = return_address

        MAR = self.ram[self.pc + 1]
        self.pc = self.reg[MAR]

    def RET(self):
        return_value = self.ram[self.sp]
        self.pc = return_value
        self.sp += 1

    def HLT(self, run):
        run = False
        return run

    def run(self):
        """Run the CPU."""
        run = True

        while run == True:
            IR = self.ram_read(self.pc)

            if IR == LDI:
                self.LDI()
                self.pc += 3
                # print("LDI")

            elif IR == PRN:
                self.PRN()
                self.pc += 2
                # print("PRN")

            elif IR == MUL or IR == ADD:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)

                self.alu(IR, reg_a, reg_b)
                self.pc += 3
                # print("ALU")

            elif IR == PUSH:
                self.PUSH()
                self.pc += 2
                # print("PUSH")

            elif IR == POP:
                self.POP()
                self.pc += 2
                # print("POP")

            elif IR == CALL:
                self.CALL()
                # print("CALL")

            elif IR == RET:
                self.RET()
                # print("RET")

            elif IR == HLT:
                run = self.HLT(run)
                # print("HLT")

            else:
                print("Error!")
                sys.exit(1)
