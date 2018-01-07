import fileinput

class TuringMachine:
    def __init__(self, state_instructions, starting_state_name):
        self.step_counter = 0
        self.current_state_name = starting_state_name
        self.states = {}
        self.cursor = 0
        self.ones = set()
        for instruction in state_instructions:
            self.states[instruction.name] = instruction

    def step(self):
        instruction = self.states[self.current_state_name]
        instruction.visit(self)
        self.step_counter += 1

    def get_current_value(self):
        return 1 if self.cursor in self.ones else 0

    def write(self, value):
        if value == 1:
            self.ones.add(self.cursor)

        elif value == 0:
            self.ones.discard(self.cursor)

        else:
            raise Exception("Nope2")

    def move(self, difference):
        self.cursor += difference

    def set_state(self, state_name):
        self.current_state_name = state_name

    def checksum(self):
        return len(self.ones)

        
            

class StateInstruction:
    def __init__(self, name, zero_write, zero_move, zero_next_state, one_write, one_move, one_next_state):
        self.name = name
        self.zero_write = zero_write
        self.zero_move = zero_move
        self.zero_next_state = zero_next_state
        self.one_write = one_write
        self.one_move = one_move
        self.one_next_state = one_next_state

    def visit(self, turing_machine):
        if turing_machine.get_current_value() == 0:
            turing_machine.write(self.zero_write)
            turing_machine.move(self.zero_move)
            turing_machine.set_state(self.zero_next_state)
        elif turing_machine.get_current_value() == 1:
            turing_machine.write(self.one_write)
            turing_machine.move(self.one_move)
            turing_machine.set_state(self.one_next_state)
        else:
            raise Exception("Nope")



def parse_puzzle_state_instruction(lines):
    # As usual, the input is meticulously well-formed.
    name = lines[0].split()[2][0]
    #print name

    zero_write = int(lines[2].split()[-1][0])
    #print zero_write
    zero_move = 1 if "right" in lines[3] else -1
    #print zero_move
    zero_next_state = lines[4].split()[-1][0]
    #print zero_next_state

    one_write = int(lines[6].split()[-1][0])
    #print one_write
    one_move = 1 if "right" in lines[7] else -1
    #print one_move
    one_next_state = lines[8].split()[-1][0]
    #print one_next_state
    #print ""

    return StateInstruction(
        name,
        zero_write, zero_move, zero_next_state,
        one_write, one_move, one_next_state
    )


def parse_blueprints(lines):
    lines = list(lines)

    first_state = lines[0].split()[-1][0]
    checksum_steps = int(lines[1].split()[-2])

    instructions = []
    for i, line in enumerate(lines):
        if "In state " in line:
            instructions.append(parse_puzzle_state_instruction(lines[i:i+9]))

    return first_state, checksum_steps, instructions


if __name__ == "__main__":
    first_state, checksum_steps, instructions = parse_blueprints(fileinput.input())

    machine = TuringMachine(instructions, first_state)

    for i in xrange(checksum_steps):
        machine.step()


    checksum = machine.checksum()
    print "Answer 1"
    print checksum

        
