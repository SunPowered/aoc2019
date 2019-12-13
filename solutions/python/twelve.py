from itertools import combinations, cycle
from collections import defaultdict

# For plotting
from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d.axes3d as plt3d
import matplotlib.animation as animation


class Planet:

        def __init__(self, init_position):

                self.position = list(init_position)
                self.velocity = [0,0,0]

        def compute_gravity(self, other):

                my_dv = [0,0,0]
                other_dv = [0,0,0]

                for i in range(3):
                        if self.position[i] > other[i]:
                                my_dv[i] -= 1
                                other_dv[i] += 1
                        elif other[i] > self.position[i]:
                                my_dv[i] += 1
                                other_dv[i] -=1

                return my_dv, other_dv

        def apply_gravity(self, dv):
                assert len(dv) == 3

                for i, dv in enumerate(dv):
                        self.velocity[i] += dv

        def step(self):
                for i, dv in enumerate(self.velocity):
                        self.position[i] += dv  

        
        def energy(self):
                return sum(map(abs, self.position)) * sum(map(abs, self.velocity))
        
        def __str__(self):
                return "<pos: x={}, y={}, z={}, vel: x={}, y={} z={}>".format(*self.position, *self.velocity)

class Simulation:

        def __init__(self, initial_positions: list):

                self.planets = [Planet(pos) for pos in initial_positions]
                self.cnt = 0  # Iteration counter

        def apply_gravity(self):

                for p_a, p_b in combinations(range(len(self.planets)), 2):

                        planet_a = self.planets[p_a]
                        planet_b = self.planets[p_b]

                        dv_a, dv_b = planet_a.compute_gravity(planet_b.position)

                        planet_a.apply_gravity(dv_a)
                        planet_b.apply_gravity(dv_b)

        def step(self, track_history=False):
                self.cnt += 1
                self.apply_gravity()
                
                for planet in self.planets:
                        planet.step()

        def run(self, n_steps: int, do_print = False):

                for i in range(n_steps):
                        self.step()

                #print()
                #print("|{}|".format(self.cnt))
                if do_print:
                        for planet in self.planets:
                                print(planet)
                        print()
                #print()

        def run2(self):
                init_positions = [planet.position for planet in self.planets]
                init_x, init_y, init_z = list(zip(*init_positions))
                init_v = tuple(0 for _ in self.planets) 

                max_count = 300000000
                
                repeats = [None, None, None]

                while self.cnt < max_count and not all(repeats):

                    if self.cnt % 100000 == 0:
                        print(self.cnt)

                    self.step()

                    cur_x, cur_y, cur_z = list(zip(*[planet.position for planet in self.planets]))
                    cur_vx, cur_vy, cur_vz = list(zip(*[planet.velocity for planet in self.planets]))
                    
                    # Check X
                    if repeats[0] is not None and cur_x == init_x and cur_vx == init_v:
                        print("X Repeat found at ", self.cnt)
                        repeats[0] = self.cnt

                    # Check y
                    if repeats[1] is not None and cur_y == init_y and cur_vy == init_v:
                        print("Y Repeat found at ", self.cnt)
                        repeats[1] = self.cnt
                    
                    # Check z
                    if repeats[2] is not None and cur_z == init_z and cur_vz == init_v:
                        print("Z Repeat found at ", self.cnt)
                        repeats[2] = self.cnt

                if self.cnt >= max_count:
                    print("Count limit exceeded: {}".format(max_count))
                else:
                    print("repeated states found at iterations: {}".format(repeats))
                
                return repeats

        def run2_better(self):


                initial_positions = [planet.position for planet in self.planets]
                init_r = init_x, init_y, init_z = tuple(zip(*initial_positions))

                repeats = []



                for i in range(3):
                    print("Checking axis: ", i)
                    self.cnt = 0

                    while True:

                        self.step()

                        cur_pos = [planet.position[i] for planet in self.planets]
                        cur_vel = [planet.velocity[i] for planet in self.planets]

                        if cur_pos == init_r[i] and cur_vel == [0,0,0]:
                            print("Found repeat for axis {}: {}".format(i, self.cnt))
                            repeats.append(self.cnt)
                            break

                print(repeats)

        def next(self, n_steps=100):
            # Returns a generator yielding successive positions

            while self.cnt < n_steps:
                self.step()
                yield tuple(pl.position for pl in self.planets)

        def calculate_energy(self):
                return sum(planet.energy() for planet in self.planets)

        def get_state(self):

                return tuple(((tuple(planet.position), tuple(planet.velocity)) for planet in self.planets))

def parse_input(input_str):
        import re

        line_re = re.compile(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>')

        positions = []

        for line in input_str.strip().split('\n'):
                # print(line)
                m = line_re.match(line.strip())
                if m is None:
                        print("Error reading line: ", line)
                assert len(m.groups()) == 3
                positions.append(tuple(map(int, m.groups())))

        return positions

def assert_state(simulation, n_runs, expected_r, expected_v):
        simulation.run(n_runs)

        for planet, exp_r, exp_v in zip(simulation.planets, expected_r, expected_v):
                assert tuple(exp_r) == tuple(planet.position), "Expected {} with position {}, got {}".format(exp_r, planet.position)
                assert tuple(exp_v) == tuple(planet.velocity), "Expected {} with velocity {}, got {}".format(exp_v, planet.velocity)


def test1():
        input_str = '''\
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
'''
        init_positions = parse_input(input_str)

        sim = Simulation(init_positions)

        assert_state(sim, 0, [(-1,0,2), (2,-10,-7), (4,-8,8), (3, 5, -1)], [(0,0,0),(0,0,0),(0,0,0),(0,0,0)])

        assert_state(sim, 1, [(2,-1,1), (3, -7, -4), (1, -7, 5), (2, 2, 0)], [(3, -1, -1),(1, 3, 3),(-3, 1, -3),(-1, -3, 1)])
        
        assert_state(sim, 8, [(5, 3, -4),(2, -9, -3),(0, -8, 4),(1, 1, 5)], [(0, 1, -2),(0, -2, 2),(0,1,-2),(0,0,2)])

        sim.run(1)

        planet_energy = sim.planets[0].energy() 
        assert  planet_energy == 36, "Expected planet energy of {}, got {}".format(36, planet_energy )
        
        sim_energy = sim.calculate_energy()
        assert sim_energy == 179, "Expected sim energy of {}, got {}".format(179, sim_energy)
        print("Tests 1 Passed")

def test2():
        input_str = '''\
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
'''
        init_positions = parse_input(input_str)

        sim = Simulation(init_positions)

        assert_state(sim, 10, [(-9, -10, 1),(4, 10, 9),(8, -10, -3),(5, -10, 3)], [(-2,-2,-1),(-3,7,-2),(5, -1, -2),(0,-4,5)])
        assert_state(sim, 90, [(8,-12,-9),(13,16,-3),(-29,-11,-1),(16,-13,23)], [(-7,3,0),(3,-11,-5),(-3,7,4),(7,1,1)])

        planet_energy = sim.planets[0].energy()
        assert  planet_energy == 290, "Expected planet energy of {}, got {}".format(290, planet_energy )

        sim_energy = sim.calculate_energy()
        assert sim_energy == 1940, "Expected sim energy of {}, got {}".format(1940, sim_energy)

        print("Tests 2 passed")

def test3():
        input_str = '''\
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
'''
        init_positions = parse_input(input_str)

        sim = Simulation(init_positions)

        counts = sim.run2()
        assert counts == 4686774924, counts

def part1():

        with open('input/12.txt') as f:
                input_str = f.read().strip()

        sim = Simulation(parse_input(input_str))

        print("Running sim 1000 steps")
        sim.run(1000)

        print("Total Energy after step 1000: ", sim.calculate_energy())

def part2():

        with open('input/12.txt') as f:
                input_str = f.read().strip()

        sim = Simulation(parse_input(input_str))

        repeats = sim.run2()
        print("Found repeats: ", repeats)
        #print("Repeated state after {} steps".format(counts))

def animate_sim():
    
    with open('input/12.txt') as f:
        input_str = f.read().strip()

    sim = Simulation(parse_input(input_str))

    f = plt.figure()
    ax = plt3d.Axes3D(f)

    points = [ax.plot(*([pi] for pi in planet.position), '*')[0] for planet in sim.planets]

    def init():
        max_size = 20
        ax.set_xlim3d([-1*max_size, max_size])
        ax.set_xlabel('x')

        ax.set_ylim3d([-1*max_size, max_size])
        ax.set_ylabel('Y')
        ax.set_zlim3d([-1*max_size, max_size])
        ax.set_zlabel('Z')

        ax.set_title("Will this animate?")

    def update(frame):
        # print(frame)
        for i, (x, y, z) in enumerate(frame):
            points[i].set_data(x, y)
            points[i].set_3d_properties(z)
        return points

    ani = animation.FuncAnimation(f, update, frames=(frame for frame in sim.next(1000)), init_func=init, interval=50)   
    plt.show()

# animate_sim()

# test1()
# test2()
# test3()
#part1() # 5937

part2()
