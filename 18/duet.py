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


class Microcontroller:

    def __init__(self, code):
        self._registers = defaultdict(int)
        self._pc = 0
        self._ticks = 0
        self.code = code
        self.sounds_played = []
        self.sounds_recovered = []

    def run_to_completion(self):
        while self._pc >= 0 and self._pc < len(self.code):
            self.tick()

    def run_to_first_rcv(self):
        while len(self.sounds_recovered) == 0:
            self.tick()

    def tick(self):
        instruction = self.code[self._pc]
        self.run_instruction(instruction)
        self._ticks += 1

    def run_instruction(self, instruction):
        print self._ticks, instruction.name, instruction.x, self.dereference(instruction.x), instruction.y
        # "Use a visitor pattern", I hear you saying. Sue me!
        getattr(self, "_isa_" + instruction.name)(instruction)

    # resolve register values or return the literal int
    def dereference(self, value):
        if is_int(value):
            return value

        return self._registers[value]
        

    ### Instruction Set ###
    def _isa_snd(self, instruction):
        sound = self.dereference(instruction.x)
        self.sounds_played.append(sound)
        self._pc += 1

    def _isa_set(self, instruction):
        target_reg = instruction.x
        value = self.dereference(instruction.y)
        self._registers[target_reg] = value
        self._pc += 1

    def _isa_add(self, instruction):
        target_reg = instruction.x
        value = self.dereference(instruction.y)
        self._registers[target_reg] += value
        self._pc += 1

    def _isa_mul(self, instruction):
        target_reg = instruction.x
        value = self.dereference(instruction.y)
        self._registers[target_reg] *= value
        self._pc += 1

    def _isa_mod(self, instruction):
        target_reg = instruction.x
        value = self.dereference(instruction.y)
        self._registers[target_reg] %= value
        self._pc += 1

    # Not clear what this does besides end the puzzle
    def _isa_rcv(self, instruction):
        conditional = self.dereference(instruction.x)
        
        if conditional == 0:
            return

        self.sounds_recovered.append(self.sounds_played[-1])
        self._pc += 1
        
    def _isa_jgz(self, instruction):
        conditional = self.dereference(instruction.x)
        if conditional <= 0:
            self._pc += 1
            return

        jump = self.dereference(instruction.y)
        self._pc += jump

        

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

    microcontroller = Microcontroller(instructions)
    microcontroller.run_to_first_rcv()

    print "Answer 1"
    print microcontroller.sounds_recovered[0]
    
    
