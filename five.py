import os

in_file = os.path.join(os.getcwd(), 'input', 'five.txt')
out_file = os.path.join(os.getcwd(), 'five_out_1.txt')

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

def debug(msg):
    if DEBUG:
        print("DEBUG -- " + msg)
        #with open(out_file, 'w') as f:
        #    f.write("DEBUG " + msg + os.linesep)

def get_val(mem: list, idx: int, mode: int = 0):
    if mode:
        # Immediate
        return mem[idx]
    else:
        # positional
        if idx < 0 :
            raise ValueError("Value of positional mode can't be negative")
        return mem[mem[idx]]

# OPCODE: 01
def add_x(mem: list, idx: int, modeflag: int):
    v1 = get_val(mem, idx + 1, modeflag & 0b001)
    v2 = get_val(mem, idx + 2, modeflag & 0b010)
    loc = get_val(mem, idx + 3, True)

    debug("{} ADD {} {} {}".format(idx, v1, v2, loc))

    mem[loc] = v1 + v2
    return idx + 4

# OPCODE: 02
def multiply_x(mem: list, idx: int, modeflag: int):
    v1 = get_val(mem, idx + 1, modeflag & 0b001)
    v2 = get_val(mem, idx + 2, modeflag & 0b010)
    loc = get_val(mem, idx + 3, True)

    debug("{} MULT {} {} {}".format(idx, v1, v2, loc))

    mem[loc] = v1 * v2
    return idx + 4

# OPCODE: 03
def op_input_x(mem: list, idx: int, modeflag: int):
    loc = get_val(mem, idx + 1, True)
    debug("{} INPUT {}".format(idx, loc))
    v1 = int(input("Enter Input: "))
    mem[loc] = v1
    return idx + 2

# OPCODE: 04
def op_output_x(mem: list, idx: int, modeflag: int):
    val = get_val(mem, idx + 1, modeflag & 0b001)
    debug("{} OUTPUT {}".format(idx, val))
    print("-- PROGRAM OUTPUT: ", val, " -- ")
    return idx + 2

# OPCODE: 05
def jit_x(mem: list, idx: int, modeflag: int):
    v1 = get_val(mem, idx + 1, modeflag & 0b001)
    loc = get_val(mem, idx + 2, modeflag & 0b010)

    debug("{} JIT {} {}".format(idx, v1, loc))

    if v1 != 0:
        idx = loc
    else:
        idx += 3
    return idx

# OPCODE: 06
def jif_x(mem: list, idx: int, modeflag: int):
    v1 = get_val(mem, idx + 1, modeflag & 0b001)
    loc = get_val(mem, idx + 2, modeflag & 0b010)

    debug("{} JIF {} {}".format(idx, v1, loc))

    if v1 == 0:
        idx = loc
    else:
        idx += 3
    return idx

# OPCODE: 07
def is_lt_x(mem: list, idx: int, modeflag: int):
    v1 = get_val(mem, idx + 1, modeflag & 0b001)
    v2 = get_val(mem, idx + 2, modeflag & 0b010)
    loc = get_val(mem, idx + 3, True)

    debug("{} ISLT {} {} {}".format(idx, v1, v2, loc))

    mem[loc] = int(v1 < v2)
        
    return idx + 4

# OPCODE: 08
def is_eq_x(mem: list, idx: int, modeflag: int):
    v1 = get_val(mem, idx + 1, modeflag & 0b001)
    v2 = get_val(mem, idx + 2, modeflag & 0b010)
    loc = get_val(mem, idx + 3, True)

    debug("{} ISEQ {} {} {}".format(idx, v1, v2, loc))

    mem[loc] = int(v1 == v2)

    return idx + 4

op_codes = {
    1: add_x,
    2: multiply_x,
    3: op_input_x,
    4: op_output_x,
    5: jit_x,
    6: jif_x,
    7: is_lt_x,
    8: is_eq_x
}

def parse_opcode(v: int):
    sv = str(v)
    if len(sv) <= 2:
        return int(sv), 0
    else:
        return int(sv[-2:]), int(sv[:-2])

def run_program(program: list):
    mem = program.copy()
    debug("Program size: {}".format(len(mem)))
    idx = 0
    while idx < len(mem):
        # debug(str(mem))
        opcode, modeflag = parse_opcode(mem[idx])
        if opcode == 99:
            print("Program Halt")
            return mem

        try:
            operation = op_codes[opcode]
        except IndexError:
            print("Bad OP Code: {}.  Exiting".format(opcode))
            return mem
        else:
            idx = operation(mem, idx, modeflag)

def test1():
    r1 =  run_program([1101, 100, -1, 4, 0])

    assert r1 == [1101, 100, -1, 4, 99]

# test1()

def test2():
    run_program([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99])
    # run_program([3,9,8,9,10,9,4,9,99,-1,8])  # Checks whether input is equal to 8, returns 1, returns 0 otherwise 
# test2()

def test3():
    # print(run_program([3,9,8,9,10,9,4,9,99,-1,8]))  # Output 1 if input is equal to 8, 0 if not
    # run_program([3,9,7,9,10,9,4,9,99,-1,8])  # Output 1 if input is less than 8, 0 otherwise
    # run_program([3,3,1108,-1,8,3,4,3,99])  # Output 1 is input is equalt to 8, using immediate mode
    # run_program([3,3,1107,-1,8,3,4,3,99])  # Output 1 if input is less than 8, 0 otherwise using immediate mode
    
    run_program([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9])  # Output 0 if the input is 0, 1 otherwise
    # This is broken when evaluating input of 0.  But why?
    # It seems as though the code is broken, specifically at memory location 2: [6, 12, 15].  Jump if False, position 12 to position 15.  Position 12 is the input provide
    # Thus if a zero is provided as input, it wants to jump to position 15, which is the last entry or '9'.  This is a bad opcode and no output ensues...  
    # I'm confused.

    # run_program([3,3,1105,-1,9,1101,0,0,12,4,12,99,1])  # Same as above, with immediate mode

    # print(run_program([1107,1,0,7,4,7,99,1]))
# test3()

def go():
    # Read program
    with open(in_file) as f:
        mem = list(map(int, f.read().strip().split(',')))

    run_program(mem)

go()

