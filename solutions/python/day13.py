import os
import aoc
import intcode
import enum
from collections import defaultdict
import time

class TileID(enum.IntEnum):

    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


@aoc.timer
def solve():

    # Setup computer
    print("Solving Day 13")
    program = list(map(int, aoc.read_program('13.txt')))
    computer = intcode.IntCodeComputer(program, pause_on_output=True)

    state = defaultdict[int]

    while computer.status != intcode.StatusFlag.FINISHED:

        # parse 3 output values
        for i in range(3):
            try:
                computer.run()
            except intcode.ProgramFinished:
                print("Program end found")
                break
        
        if computer.status != intcode.StatusFlag.FINISHED:
            x, y, t_id = computer.output_value
            computer.output_value = None

            state[(x, y)] = t_id

    total_block_tiles = sum([t_id == TileID.BLOCK.value for t_id in state.values()])
    print(f"Total Blocks: {total_block_tiles}")


class Game:

    def __init__(self, board_dim=(25,25), ai=False):
        self.automated = ai
        game_input = self.game_input()
        next(game_input)
        program = list(map(int, aoc.read_program('13.txt')))
        program[0] = 2  # Set up for unlimited play

        self.computer = intcode.IntCodeComputer(program, input_user = game_input, pause_on_output=True)
        
        self.state = defaultdict(int)
        self.score = 0
        self.last_input = None
        self.board_dim = board_dim
        self.char_map = {
            0: ' ',
            1: '\u2588',
            2: '\u2591',
            3: '\u2501',
            4: '\u25cf' 
        }

    def find_board_dim(self):
        # Find max x and y values in state
        max_x = max_y = -1

        for (x, y) in self.state:
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
        return max_x+1, max_y+1

    def print_board(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        dim_x, dim_y = self.find_board_dim()
        for i in range(dim_y):

            row = "".join([self.char_map[self.state[(j, i)]] for j in range(dim_x)])
            print(row)
            
            #if (self.char_map[3] in row) or (self.char_map[4] in row):
            # Are there any characters not a wall or a block?
            #    import pdb; pdb.set_trace()

        print(f"Score: {self.score}\n")

    def game_input(self):
        yield None  # Define the generator before the logic begins

        while True:
            self.print_board()
            if self.automated:
                user_input = self.calculate_best_move()
                # time.sleep(0.05)
            else:
                user_input = input("Enter joystick input: ")
                try:
                    user_input = int(user_input)
                except ValueError:
                    user_input = self.last_input or 0

                self.last_input = user_input
            
            yield user_input

    def calculate_best_move(self):

        try:
            paddle_pos = [k for k,v in self.state.items() if v == 3][0]
            ball_pos = [k for k,v in self.state.items() if v == 4][0]
        except ValueError:
            return  0

        # Crude Strategy is to ensure paddle is below ball

        if paddle_pos[0] > ball_pos[0]:
            return -1
        elif paddle_pos[0] < ball_pos[0]:
            return 1
        else:
            return 0

    def play(self):
        print("\nLoading Game\n")
        while self.computer.status != intcode.StatusFlag.FINISHED:
        
            # parse 3 output values           
            for i in range(3):
                try:
                    self.computer.run()
                except intcode.ProgramFinished:
                    print("Program end found")
                    break

            if self.computer.status != intcode.StatusFlag.FINISHED:
                x, y, t_id = self.computer.output_value
                self.computer.output_value = None
                
                if (x, y) != (-1, 0):
                    self.state[(x, y)] = t_id
                else:
                    self.score=t_id

        print(f"Final Score: {self.score}")
# solve()

game = Game(ai=True)
aoc.timer(game.play())