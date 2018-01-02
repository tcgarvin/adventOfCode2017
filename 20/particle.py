import fileinput
import re
from collections import defaultdict

# Could go get VPython or any of the several math libs, but we'll hack it with
# stock python for now
class ParticleState:

    # Maybe I'm just getting tired, but parsing this without regex
    PARTICLE_RE = re.compile("""
        p=<(?P<x>[^,]*),(?P<y>[^,]*),(?P<z>[^>]*)>,\s*
        v=<(?P<vx>[^,]*),(?P<vy>[^,]*),(?P<vz>[^>]*)>,\s*
        a=<(?P<ax>[^,]*),(?P<ay>[^,]*),(?P<az>[^>]*)>
    """, re.X)

    @classmethod
    def from_puzzle_input(cls, i, line):
        match = cls.PARTICLE_RE.search(line)

        groups = match.groupdict()

        return ParticleState(
            i,
            int(groups["x"]),
            int(groups["y"]),
            int(groups["z"]),
            int(groups["vx"]),
            int(groups["vy"]),
            int(groups["vz"]),
            int(groups["ax"]),
            int(groups["ay"]),
            int(groups["az"]))
        

    def __init__(self, i, x,y,z,vx,vy,vz,ax,ay,az):
        self.number = i
        self.x=x
        self.y=y
        self.z=z
        self.vx=vx
        self.vy=vy
        self.vz=vz
        self.ax=ax
        self.ay=ay
        self.az=az

    def __str__(self):
        return "%s: p=<%s,%s,%s>, v=<%s,%s,%s>, a=<%s,%s,%s>" % (self.number, self.x, self.y, self.z, self.vx, self.vy, self.vz, self.ax, self.ay, self.az)


def find_long_term_closest(p_states):
    # The assumption here is that acceleratin dominates, so we'll just find the
    # smallest acceleration.

    smallest_acceleration = 1000
    candidate = None
    for state in p_states:
        manhattan_acceleration = abs(state.ax) + abs(state.ay) + abs(state.az)
        if manhattan_acceleration < smallest_acceleration:
            smallest_acceleration = manhattan_acceleration
            candidate = state
            print "Smallest", manhattan_acceleration, state.number, state

        elif manhattan_acceleration == smallest_acceleration:
            print "Dupe", manhattan_acceleration, state.number, state

    return candidate


def simulate_one_tick(state):
    state.vx += state.ax
    state.vy += state.ay
    state.vz += state.az
    state.x += state.vx
    state.y += state.vy
    state.z += state.vz


def simulate_with_collisions(p_states):
    time = 0
    time_since_last_collision = 0
    remaining_p_states = {state.number: state for state in p_states}
    while time_since_last_collision < 1000:
        collision_index = defaultdict(list)
        for state in p_states:
            simulate_one_tick(state)
            collision_position = collision_index[(state.x, state.y, state.z)]
            collision_position.append(state)

            if len(collision_position) > 1:
                print "Collision.  Time since last:", time_since_last_collision
                time_since_last_collision = 0
                for colliding_state in collision_position:
                    removed = remaining_p_states.pop(colliding_state.number, None)
                    if removed is not None:
                        print "Neutralized", removed

        if time_since_last_collision == 0:
            print len(remaining_p_states), "remaining"
        time_since_last_collision += 1
        time += 1

    return len(remaining_p_states)


def parse_particle_states(lines):
    return map(lambda pair: ParticleState.from_puzzle_input(pair[0], pair[1]), enumerate(lines))

    

if __name__ == "__main__":
    p_states = parse_particle_states(fileinput.input())

    closest = find_long_term_closest(p_states)

    print "Answer 1 can be derived by looking at the above debug statements"
    print ""

    remaining_after_collisions = simulate_with_collisions(p_states)

    print "Answer 2"
    print remaining_after_collisions
