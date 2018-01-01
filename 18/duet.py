import fileinput
from collections import defaultdict
from Queue import Queue, Empty

def is_int(value):
    try:
        int(value)
        return True

    except TypeError:
        return False

    except ValueError:
        return False


class Microcontroller:

    def __init__(self, program_id, code, input_queue, output_queue):
        self._registers = defaultdict(int)
        self._registers["p"] = program_id
        self.pid = program_id
        self._pc = 0
        self._ticks = 0
        self.code = code
        self._outbound = output_queue
        self._inbound = input_queue
        self.sent = 0
        self.waiting = False


    def is_complete(self):
        return self._pc < 0 or self._pc >= len(self.code)


    def can_progress(self):
        return not self.is_complete() and (not self.waiting or not self._inbound.empty())
        

    def run_to_completion(self):
        while not self.is_complete():
            self.tick()


    def run_to_first_wait(self):
        while self.can_progress():
            self.tick()


    def tick(self):
        instruction = self.code[self._pc]
        self.run_instruction(instruction)
        if not self.waiting:
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


    def _isa_snd(self, instruction):
        to_send = self.dereference(instruction.x)
        self._outbound.put(to_send, False)
        self.sent += 1
        self._pc += 1
        self._log("Sent", to_send)


    def _isa_rcv(self, instruction):
        received = None
        try:
            received = self._inbound.get(False)
        except Empty:
            pass

        if received is None:
            self.waiting = True
            return

        self.waiting = False
        self._registers[instruction.x] = received
        self._pc += 1
        self._log("Got ", received)
        

    def _isa_jgz(self, instruction):
        conditional = self.dereference(instruction.x)
        if conditional <= 0:
            self._pc += 1
            return

        jump = self.dereference(instruction.y)
        self._pc += jump


    def _log(self, *items):
        to_print = [("\t\t\t" * self.pid)] + list(items)
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


def run_programs_to_completion(prog_a, prog_b):
    while prog_a.can_progress() or prog_b.can_progress():
        prog_a.run_to_first_wait()
        prog_b.run_to_first_wait()



def parse_input(lines):
    return [Instruction.from_puzzle_input(l) for l in lines]


if __name__ == "__main__":
    instructions = parse_input(fileinput.input())

    output = Queue()
    microcontroller = Microcontroller(0, instructions, Queue(), output)
    microcontroller.run_to_first_wait()

    last_output = None
    while not output.empty():
        last_output = output.get(False)

    print "Answer 1"
    print last_output

    q0to1 = Queue()
    q1to0 = Queue()
    program0 = Microcontroller(0, instructions, q1to0, q0to1)
    program1 = Microcontroller(1, instructions, q0to1, q1to0)

    run_programs_to_completion(program0, program1)

    print "Answer 2"
    print program1.sent
    
    
