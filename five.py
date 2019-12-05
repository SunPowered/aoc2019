import os

in_file = os.path.join(os.getcwd(), 'input', 'five.txt')

assert os.path.exists(in_file), "Expecting input file: {}".format(in_file)

"""
Intcode computer again.  This time with some extra requirements.  

I am going to code it back from scratch this time.

The OPCODE commands are:
    1 - Addition | 1, 2, 3, 4 -> Add values from position 2 and 3, save to position 4
    2 - Multiplication | 2, 1, 3, 4 -> Multiply values from position 1 and 3, save to position 4
    3 - Save value to position | 3, 50, 4 -> Save value 4 to position 50
    4 - Output a value | 4, 50 -> Output the value at position 50
    99 - Exit


Additionally, OPCODE commands are prefixed with binary code to specify the parameter mode to operate.  THere are two modes, position mode and immediate mode.  Position mode is to interpret the bit as a memory (position) location, immediate takes the value literally.

Immediate values can be any integer, positive or negative.  Positional are only able to be postive integers.

OPCODES are coded as 4 or 5 bit values: The last 2 digits are the opcode, and the remaining preface digits are interpreted as flags for immediate mode of the various parameters.  No value assumes a 0.
"""
DEBUG = True

def get_val(mem, p, mode):
    if mode:
        return p
    else:
        if p < 0 :
            raise ValueError("Value of positional mode can't be negative")
        return mem[p]

# OPCODE: 01
def add(mem: list, p1: int, p2: int, p3: int, mode_flag=0b000):
    v1 = get_val(mem, p1, mode_flag & 0b001)
    v2 = get_val(mem, p2, mode_flag & 0b010)
    mem[p3] = v1 + v2
    
# OPCODE: 02
def multiply(mem: list, p1: int, p2: int, p3: int, mode_flag=0b000):
    v1 = get_val(mem, p1, mode_flag & 0b001)
    v2 = get_val(mem, p2, mode_flag & 0b010)
    mem[p3] = v1 * v2

# OPCODE: 03
def op_input(mem: list, p1: int, mode_flag=0b000):
    # Get input?
    v1 = int(input("Provide Integer Input: "))
    mem[p1] = v1

# OPCODE: 04
def op_output(mem: list, p1: int, mode_flag=0b000):
    # Return output?
    v1 = get_val(mem, p1, mode_flag & 0b001)
    print("Output: ", v1)

# OPCODE: 05
def jump_if_true(mem: list, p1:int, p2: int, mode_flag=0b000):
    v1 = get_val(mem, p1, mode_flag & 0b001)
    if v1 is not 0:
        return p2
    return None

# OPCODE: 06
def jump_if_false(mem: list, p1: int, p2: int, mode_flag=0b000):
    v1 = get_val(mem, p1, mode_flag & 0b001)
    if v1 == 0:
        return p2
    return None

# OPCODE: 07
def is_less_than(mem: list, p1: int, p2: int, p3: int, mode_flag=0b000):
    v1 = get_val(mem, p1, mode_flag & 0b001)
    v2 = get_val(mem, p2, mode_flag & 0b010)
    mem[p3] =  int(v1 < v2)
        
# OPCODE: 08
def is_equals(mem: list, p1: int, p2: int, p3: int, mode_flag=0b000):
    v1 = get_val(mem, p1, mode_flag & 0b001)
    v2 = get_val(mem, p2, mode_flag & 0b010)
    mem[p3] = int(v1 == v2)

def parse_opcode(v: int):
    sv = str(v)
    if len(sv) <= 2:
        return int(sv), 0
    else:
        return int(sv[-2:]), int(sv[:-2])

def debug(msg):
    if DEBUG:
        print(msg)

def run_program(program: list):
    mem = program.copy()
    debug("Program length: {}".format(len(mem)))
    idx = 0
    while idx < len(mem):
        opcode, modeflag = parse_opcode(mem[idx])
        debug("OP_MODE: {} {} | {}".format(idx, opcode, modeflag))
        if opcode == 1:
            p1, p2, p3 = mem[idx+1:idx+4]
            debug("Add: {} {} {}".format(p1, p2, p3))
            add(mem, p1, p2, p3, modeflag)
            idx += 4

        elif opcode == 2:
            p1, p2, p3 = mem[idx+1:idx+4]
            debug("Multiply: {} {} {}".format(p1, p2, p3))
            multiply(mem, p1, p2, p3, modeflag)
            idx += 4

        elif opcode == 3:
            p1 = mem[idx+1]
            debug("Input: {}".format(p1))
            op_input(mem, p1)
            idx += 2

        elif opcode == 4:
            p1 = mem[idx + 1]
            debug("Output: {}".format(p1))
            op_output(mem, p1, modeflag)
            idx += 2

        elif opcode == 5:
            p1, p2 = mem[idx + 1: idx+3]
            debug("Jump if true: {} {}".format(p1, p2))
            ret = jump_if_true(mem, p1, p2, modeflag)
            if ret is not None:
                idx = ret
            else:
                idx += 3

        elif opcode == 6:
            p1, p2 = mem[idx+1: idx + 3]
            debug("Jump if false: {} {}".format(p1, p2))
            ret = jump_if_false(mem, p1, p2, modeflag)
            if ret is not None:
                idx = ret
            else:
                idx += 3

        elif opcode == 7:
            p1, p2, p3 = mem[idx + 1: idx + 4]
            debug("Less than: {} {} {}".format(p1, p2, p3))
            is_less_than(mem, p1, p2, p3, modeflag)
            idx += 4

        elif opcode == 8:
            p1, p2, p3 = mem[idx + 1: idx + 4]
            debug("Is Equals: {} {} {}".format(p1, p2, p3))
            is_equals(mem, p1, p2, p3, modeflag)
            idx += 4

        elif opcode == 99:
            debug("Program Break")
            break
        
        else:
            print("Bad opcode: {}. Exiting".format(opcode))
            break
    return mem

def test1():
    r1 =  run_program([1101, 100, -1, 4, 0])

    assert r1 == [1101, 100, -1, 4, 99]

# test1()

def test2():
    r1 = run_program([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99])
    # run_program([3,9,8,9,10,9,4,9,99,-1,8])
# test2()

def go():
    # Read program
    with open(in_file) as f:
        mem = list(map(int, f.read().strip().split(',')))

    run_program(mem)

go()

