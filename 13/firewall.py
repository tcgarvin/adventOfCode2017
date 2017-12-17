import fileinput

class Layer:
    def __init__(self, scan_range):
        self.scan_range = scan_range
        self.reset()


    def at_pos(self,index):
        return self.curs == index


    def tick(self):
        if self.dir == "forward" and self.curs == self.scan_range - 1:
            self.dir = "backward"

        elif self.dir == "backward" and self.curs == 0:
            self.dir = "forward"

        self.curs += 1 if self.dir == "forward" else -1


    def reset(self):
        self.curs = 0
        self.dir = "forward"


    def get_range(self):
        return self.scan_range


    def __repr__(self):
        return "Layer(%s) -> %s %s" % (self.scan_range, self.curs, self.dir)



class NoneLayer(Layer):
    def __init__(self):
        pass

    def at_pos(self, index):
        return False

    def tick(self):
        pass

    def reset(self):
        pass

    def get_range(self):
        return 0

NONE_LAYER = NoneLayer()
        


class Firewall:
    def __init__(self):
        self.layers = {}


    def add_layer(self, position, layer):
        self.layers[position] = layer
        

    def tick(self):
        for layer in self.layers.itervalues():
            layer.tick()


    def reset(self):
        for layer in self.layers.itervalues():
            layer.reset()
        

    def security_check(self, position):
        severity = 0
        layer = self.layers.get(position, NONE_LAYER)
        if layer.at_pos(0):
            severity = position * layer.get_range()
            #print severity, position, layer
        return severity


    def num_layers(self):
        return max(self.layers.iterkeys())
            
    

def parse_firewall(lines):
    firewall = Firewall()
    for line in lines:
        position, scan_range = map(int, line.strip().split(": "))
        firewall.add_layer(position, Layer(scan_range))

    return firewall


def severity_for_crossing(firewall):
    severity = 0
    for position in xrange(firewall.num_layers()):
        severity += firewall.security_check(position)
        firewall.tick()

    return severity


# XXX: Didn't track being caught seperately from the severity value, so need to rework that
def find_delay_for_safe_crossing(firewall):
    found_safe_passage = False
    delay = -1
    while not found_safe_passage:
        delay += 1
        firewall.reset()
        for t in xrange(delay):
            firewall.tick()

        sev = severity_for_crossing(firewall)
        print delay, sev
        if sev == 0:
            found_safe_passage = True

    return delay


if __name__ == "__main__":
    firewall = parse_firewall(fileinput.input())

    #print severity_for_crossing(firewall)

    print find_delay_for_safe_crossing(firewall)
