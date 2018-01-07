import fileinput

class Layer:
    def __init__(self, scan_range):
        self.scan_range = scan_range
        

    def cycle_time(self):
        return (self.scan_range - 1) * 2


    def present_at(self, time):
        return time % self.cycle_time() == 0


    def get_range(self):
        return self.scan_range


    def __repr__(self):
        return "Layer(%s)" % (self.scan_range,)



class NoneLayer(Layer):
    def __init__(self):
        pass

    def cycle_time(self):
        return 0

    def present_at(self, time):
        return False

    def get_range(self):
        return 0

    def __repr__(self):
        return "NoneLayer()"

NONE_LAYER = NoneLayer()
        


class Firewall:
    def __init__(self):
        self.layers = {}


    def add_layer(self, position, layer):
        self.layers[position] = layer
        

    def security_check(self, position, time):
        caught = False
        severity = 0
        layer = self.layers.get(position, NONE_LAYER)
        if layer.present_at(time):
            caught = True
            severity = position * layer.get_range()
        #print position, time, layer, caught, severity
        return caught, severity


    def num_layers(self):
        return max(self.layers.iterkeys()) + 1
            
    

def parse_firewall(lines):
    firewall = Firewall()
    for line in lines:
        position, scan_range = map(int, line.strip().split(": "))
        firewall.add_layer(position, Layer(scan_range))

    return firewall


def severity_for_crossing(firewall, time):
    caught = False
    severity = 0
    for position in xrange(firewall.num_layers()):
        position_caught, position_severity = firewall.security_check(position, position + time)
        caught |= position_caught
        severity += position_severity

    return caught, severity


def is_crossing_clean(firewall, time):
    for position in xrange(firewall.num_layers()):
        position_caught, position_severity = firewall.security_check(position, position + time)
        if position_caught:
            return False

    return True


def find_clean_delay(firewall):
    delay = 0
    while not is_crossing_clean(firewall, delay):
        delay += 1

    return delay


if __name__ == "__main__":
    firewall = parse_firewall(fileinput.input())

    caught, severity = severity_for_crossing(firewall, 0)

    print "Answer 1"
    print severity
    print ""
    delay = find_clean_delay(firewall)
    print "Answer 2"
    print delay
