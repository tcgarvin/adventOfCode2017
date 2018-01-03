import fileinput
from collections import defaultdict

def is_int(value):
    try:
        int(value)
        return True

    except TypeError:
        return False

    except ValueError:
        return False


class Coprocessor:

    def __init__(self, code):
        self._registers = defaultdict(int)
        self._pc = 0
        self._ticks = 0
        self.code = code
        self.mul_count = 0


    def is_complete(self):
        return self._pc < 0 or self._pc >= len(self.code)


    def can_progress(self):
        return not self.is_complete()
        

    def run_to_completion(self):
        while not self.is_complete():
            self.tick()


    def tick(self):
        instruction = self.code[self._pc]
        self.run_instruction(instruction)
        self._ticks += 1


    def run_instruction(self, instruction):
        self._log(self._ticks, instruction.name, instruction.x, instruction.y)
        getattr(self, "_isa_" + instruction.name)(instruction)


    # resolve register values or return the literal int
    def dereference(self, value):
        if is_int(value):
            return value

        return self._registers[value]
        

    ### Instruction Set ###
    def _isa_set(self, instruction):
        target_reg = instruction.x
        value = self.dereference(instruction.y)
        self._registers[target_reg] = value
        self._pc += 1


    def _isa_sub(self, instruction):
        target_reg = instruction.x
        value = self.dereference(instruction.y)
        self._registers[target_reg] -= value
        self._pc += 1


    def _isa_mul(self, instruction):
        target_reg = instruction.x
        value = self.dereference(instruction.y)
        self._registers[target_reg] *= value
        self._pc += 1
        self.mul_count += 1


    def _isa_jnz(self, instruction):
        conditional = self.dereference(instruction.x)
        if conditional != 0:
            self._pc += 1
            return

        jump = self.dereference(instruction.y)
        self._pc += jump


    def _log(self, *items):
        to_print = list(items)
        print(" ".join(map(str,to_print)))

        

class Instruction:

    @classmethod
    def from_puzzle_input(cls, input_line):
        tokens = input_line.split()
        name = tokens[0]
        x = tokens[1]
        y = None
        if len(tokens) >= 3:
            y = tokens[2]

        if is_int(y):
            y = int(y)

        return Instruction(name, x, y)
        

    def __init__(self, name, x, y = None):
        self.name = name
        self.x = x
        self.y = y



def parse_input(lines):
    return [Instruction.from_puzzle_input(l) for l in lines]


if __name__ == "__main__":
    instructions = parse_input(fileinput.input())

    program = Coprocessor(instructions)
    program.run_to_completion()

    print "Answer 1"
    print program.mul_count

