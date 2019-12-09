from typing import List
from enum import Enum

class DebugFlag(Enum):
    OFF = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    EXTREME = 4

class ModeFlag(Enum):
    Positional = 0
    Immediate = 1
    Relative = 2

class StatusFlag(Enum): 
    READY = 0
    FINISHED = 1
    PAUSED = 2

class ArgumentError(Exception):
    pass

class IntCodeComputer:

    def __init__(self, program: List[int], input_user=None, debug=DebugFlag.OFF, pause_on_output: bool=False):
        """
        An IntCode Computer.

        Arguments:
            program: The program to run, this should be a list of ints
            input_user: A flag to tell the computer how to get input.  Leaving it None prompts the user in real time for an input.  Otherwise, the value is converted to an int and used.
                        This is useful for testing the computer with known programs and inputs
            debug_level: A debug flag to spit out more information.  Higher levels are more verbose, 0 is off.
            pause_on_output: A boolean flag to enable breaking the program on an output command. 
        """
        self.program = program  # Store the original program for reference
        self.memory = program.copy()  # Copy it to memory for working
        
        self.set_input_values(input_user)
        self.debug_flag = debug
        self.pause_on_output = pause_on_output
        self.status = StatusFlag.READY   # This is set to indicate a progam break, or pause
        self.idx = 0                     # The instruction pointer
        self.relative_base = 0           # The relative address base
        self.output_value = None
        self.op_codes = {
            1: self.add_x,
            2: self.multiply_x,
            3: self.input_x,
            4: self.output_x,
            5: self.jump_if_true_x,
            6: self.jump_if_false_x,
            7: self.is_less_than_x,
            8: self.is_equals_x
        }

    def debug(self, msg: str, level: int):
        if level.value <= self.debug_flag.value:
            print("D{} -- {}".format(level.value, msg))

    def set_input_values(self, input_vals):
        if not hasattr(input_vals, '__iter__'):
            input_vals = [input_vals]
        self.input_user = (i for i in input_vals)

    def set_program(self, program: List[int]):
        # Reset the program
        self.program = program
        self.mem = program.copy()
        self.output_value = None
        self.idx = 0
        self.status = StatusFlag.READY

    def get_value(self, idx: int, mode: ModeFlag = ModeFlag.Positional):
        if idx < 0:
            raise ValueError("Bad address location: {}".format(idx))
        
        value = self.mem[idx]  # The value at the idx pointer

        if mode == ModeFlag.Positional:        
            # Return the value at the address 'value'
            if value < 0:
                raise ValueError("Bad Positional Address Value: {}".format(value))
            return self.mem[value]
        elif mode == ModeFlag.Immediate:
            # Return the value itself
            return value
        elif mode == ModeFlag.Relative:
            # This takes the value at a relative position to the base, by the amount of the argument
            return self.relative_base + value

    def parse_opcode(self, v: int):
        # This parses an integer input, splits the opcode and the mode_flag
        # This mode_flag can be 0 - 3 digits long, each digit must be representable by the enum ModeFlag
        
        sv = str(v)
        if len(sv) <= 2:
            # No mode parameters
            return int(sv), []
        else:
            # Mode parameters present, parse into ModeFlag enums
            modes = [ModeFlag(int(mode_flag)) for mode_flag in sv[:-2][::-1]]
            return int(sv[-2:]), modes

    def get_arguments(self, n_args: int, modes: List[ModeFlag]):
        if n_args > 3:
            raise ValueError("Max arguments are 3")

        if len(modes) != n_args:
            raise ValueError("Length modes ({}) must be same number of arguments as requested ({})".format(len(modes), n_args))

        return (self.get_value(self.idx + 1 + i, modes[i]) for i in range(n_args))

    def run(self, input_vals=None, debug: int=None):
        if input_vals is not None:
            self.set_input_values(input_vals)

        if debug is not None:
            self.debug_flag = debug

        self.debug("Running Program:  Size -> {}".format(len(self.program)), DebugFlag.LOW)
        self.debug(self.program, DebugFlag.MEDIUM)
        # If the status is already set, then we are resuming.  Otherwise, initialize the run
        if self.status is StatusFlag.READY or self.status is StatusFlag.FINISHED:
            self.mem = self.program.copy()  # Load memory with program
            self.idx = 0
        
        self.status = StatusFlag.READY
        while self.idx < len(self.program) and self.status is StatusFlag.READY:
            self.debug(str(self.mem), DebugFlag.EXTREME)
            opcode, modeflag = self.parse_opcode(self.mem[self.idx])
            if opcode == 99:
                self.debug("Program Halt", DebugFlag.LOW) 
                self.status = StatusFlag.FINISHED
                break
            try:
                operation = self.op_codes[opcode]
            except IndexError:
               print("Bad OP Code: {}.  Exiting".format(opcode))
            else:
                operation(modeflag)

    def _pad_modeflag(self, modes: List[ModeFlag], n: int, v: ModeFlag=ModeFlag.Positional):
        # This is to ensure that the mode list is the right length.
        # For example, if no modes are given, we still need to pass a mode flag parameter  
        # Some operations require 

        modes.extend([v]*(n - len(modes)))
        return modes

    def _pre_operation(self, modeflag: List[ModeFlag], n_args: int, writable_operation=True)-> List[int]:
        # If writable operation, the last element must be Immediate
        modeflag = self._pad_modeflag(modeflag, n_args)

        if writable_operation:
            modeflag[-1] = ModeFlag.Immediate

        self.debug(self.mem[self.idx:self.idx+n_args+1], DebugFlag.HIGH)
        
        assert len(modeflag) == n_args
        return self.get_arguments(n_args, modeflag)

    # OPCODE: 01
    def add_x(self, modeflag: List[ModeFlag]):
        v1, v2, loc = self._pre_operation(modeflag, 3)
        self.mem[loc] = v1 + v2
        self.idx += 4

    # OPCODE: 02 
    def multiply_x(self, modeflag: int):
        v1, v2, loc = self._pre_operation(modeflag, 3)
        self.debug("|{}| MULT: {} * {} -> [{}]".format(self.idx, v1, v2, loc), DebugFlag.MEDIUM)
        self.mem[loc] = v1 * v2
        self.idx += 4

    # OPCODE: 03
    def input_x(self, modeflag: int):
        loc, = self._pre_operation(modeflag, 1)
        self.debug("|{}| INP: -> [{}]".format(self.idx, loc), DebugFlag.MEDIUM)

        if self.input_user is not None:
            try:
                v = int(next(self.input_user))
            except StopIteration:
                # we reached the end of the given user inputs, pause the program to wait for additional input to be set
                self.status = StatusFlag.PAUSED
                return
        else:
            v = int(input("Enter Input Value: "))

        self.mem[loc] = v
        self.idx += 2

    # OPCODE: 04
    def output_x(self, modeflag: int):
        v, = self._pre_operation(modeflag, 1, writable_operation=False)
        self.debug("|{}| OUT {}".format(self.idx, v), DebugFlag.MEDIUM)
        self.debug("!! Program Output: {} !!".format(v), DebugFlag.LOW)
        self.output_value = v
        self.idx += 2

        if self.pause_on_output:
            self.status = StatusFlag.PAUSED

    # OPCODE: 05
    def jump_if_true_x(self, modeflag: int):
        v1, loc = self._pre_operation(modeflag, 2, writable_operation=False)
        self.debug("|{}| JIT {} -> [{}]".format(self.idx, v1, loc), DebugFlag.MEDIUM)

        if v1 != 0:
            self.idx = loc
        else:
            self.idx += 3

    # OPCODE: 06
    def jump_if_false_x(self, modeflag: int):
        v1, loc = self._pre_operation(modeflag, 2, writable_operation=False)
        self.debug("|{}| JIF {} -> [{}]".format(self.idx, v1, loc), DebugFlag.MEDIUM)

        if v1 == 0:
            self.idx =loc
        else:
            self.idx += 3

    # OPCODE: 07
    def is_less_than_x(self, modeflag: int):
        v1, v2, loc = self._pre_operation(modeflag, 3)
        self.debug("|{}| ISLT {} {} -> [{}]".format(self.idx, v1, v2, loc), DebugFlag.MEDIUM)

        self.mem[loc] = int( v1 < v2 )
        self.idx += 4

    # OPCODE: 08
    def is_equals_x(self, modeflag: int):
        v1, v2, loc = self._pre_operation(modeflag, 3)
        self.debug("|{}| ISEQ {} {} -> [{}]".format(self.idx, v1, v2, loc), DebugFlag.MEDIUM)

        self.mem[loc] = int( v1 == v2 )
        self.idx += 4


##  Tests

def assert_program_memory(program:List[int], input_val, expected_output: List[int], debug: int=DebugFlag.OFF):
    computer = IntCodeComputer(program, input_user=input_val, debug=debug)
    computer.run()
    assert computer.mem == expected_output, "Unexpected memory state after running program"

def assert_program_output(program: List[int], input_val, expected_output: int, debug: int=DebugFlag.OFF):
    computer = IntCodeComputer(program, input_user=input_val, debug=debug)
    computer.run()

    assert computer.output_value == expected_output, "Unexpected Output Value"


def tests_day2():
    # Day 2 tests
    debug = DebugFlag.OFF
    
    assert_program_memory([1,9,10,3,2,3,11,0,99,30,40,50], None, [3500,9,10,70,2,3,11,0,99,30,40,50], debug)

    assert_program_memory([1,0,0,0,99], None, [2,0,0,0,99], debug=debug)
    assert_program_memory([2,3,0,3,99], None, [2,3,0,6,99], debug=debug)
    assert_program_memory([2,4,4,5,99,0], None, [2,4,4,5,99,9801], debug=debug)
    assert_program_memory([1,1,1,4,99,5,6,0,99], None, [30,1,1,4,2,5,6,0,99], debug=debug)

    print("Day 2 tests passed!")

def tests_day5():
    # Day 5 tests
    debug = DebugFlag.OFF
    assert_program_output([3,9,8,9,10,9,4,9,99,-1,8], 8, 1, debug=debug)
    assert_program_output([3,9,8,9,10,9,4,9,99,-1,8], 7, 0, debug=debug)

    assert_program_output([3,9,7,9,10,9,4,9,99,-1,8], 7, 1, debug=debug)
    assert_program_output([3,9,7,9,10,9,4,9,99,-1,8], 9, 0, debug=debug)

    assert_program_output([3,3,1108,-1,8,3,4,3,99], 8, 1, debug=debug)
    assert_program_output([3,3,1108,-1,8,3,4,3,99], 2, 0, debug=debug)

    assert_program_output([3,3,1107,-1,8,3,4,3,99], 1, 1, debug=debug)
    assert_program_output([3,3,1107,-1,8,3,4,3,99], 9, 0, debug=debug)

    # jump tests
    assert_program_output([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 0, 0, debug=debug)
    assert_program_output([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 2, 1, debug=debug)

    assert_program_output([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 0, 0, debug=debug)
    assert_program_output([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 2, 1, debug=debug)

    assert_program_output([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31, 
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 7, 999, debug=debug)
    
    assert_program_output([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 8, 1000, debug=debug)

    assert_program_output([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 9, 1001, debug=debug)

    print("Day 5 tests passed")


def tests_day7():
    # We need to handle multiple inputs
    debug = DebugFlag.OFF
    assert_program_output([3, 11, 3, 12, 1, 11, 12, 13, 4, 13, 99, -1 , -1, 9], (3, 5), 8, debug=debug)  # Add two input numbers together and output result
    assert_program_output([3, 11, 3, 12, 1, 11, 12, 13, 4, 13, 99, -1 , -1, 9], (4, 7), 11, debug=debug)
    print("Day 7 tests passed")

def run_all_tests():
    tests_day2()
    tests_day5()
    tests_day7()

run_all_tests()