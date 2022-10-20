import copy
import os
from typing import Type
from termcolor import colored, cprint
from rule_based_ai import Rule_AI
from minimax_ai import Minimax_AI
from neat_ai import Neat_AI_Wrapper
import time
import threading
import pickle

class Board:
    def __init__(self):
        self.whitechar = 'W'
        self.blackchar = 'B'
        self.last_ai_move = (-1, -1)
        self.ai = [Minimax_AI()]
        self.board = [['-' for i in range(8)] for j in range(8)]
        self.colormap = [['green', 'green', 'green', 'green', 'green', 'green', 'green', 'green'],
                         ['green', 'red',   'red',   'red',   'red',   'red',   'red',   'green'],
                         ['green', 'red',   'cyan',  'cyan',  'cyan',  'cyan',  'red',   'green'],
                         ['green', 'red',   'cyan',  'cyan',  'cyan',  'cyan',  'red',   'green'],
                         ['green', 'red',   'cyan',  'cyan',  'cyan',  'cyan',  'red',   'green'],
                         ['green', 'red',   'cyan',  'cyan',  'cyan',  'cyan',  'red',   'green'],
                         ['green', 'red',   'red',   'red',   'red',   'red',   'red',   'green'],
                         ['green', 'green', 'green', 'green', 'green', 'green', 'green', 'green']]
                         
        self.board[3][3] = self.whitechar
        self.board[3][4] = self.blackchar
        self.board[4][3] = self.blackchar
        self.board[4][4] = self.whitechar

    def __str__(self):
        return '\n'.join([' '.join(row) for row in self.board])
    
    def print_self(self, moves=[]):
        board_to_print = copy.deepcopy(self.board)

        print("\n" + "┌──" + ("┬──" * (7)) + "┐")

        for row in range(8):
            if row != 0:
                print("\n" + "├──" + ("┼──" * (7)) + "┤" + " ")

            print("│", end="")
            for col in range(8):
                if board_to_print[row][col] != self.blackchar and board_to_print[row][col] != self.whitechar and board_to_print[row][col] == '-':
                    print(colored(board_to_print[row][col], self.colormap[row][col]) * 2, end="")
                elif board_to_print[row][col] != self.blackchar and board_to_print[row][col] != self.whitechar and board_to_print[row][col] != '-':
                    print(colored(board_to_print[row][col], self.colormap[row][col]), end="")
                elif board_to_print[row][col] == self.blackchar and self.last_ai_move[0] == row and self.last_ai_move[1] == col:
                    print(colored('⬤ ', 'grey'), end="")
                elif board_to_print[row][col] == self.blackchar:
                    print(colored(board_to_print[row][col], 'grey', 'on_grey') * 2, end="")
                elif board_to_print[row][col] == self.whitechar:
                    print(colored(board_to_print[row][col], 'white', 'on_white') * 2, end="")
                print("│", end="")
            print(" " + str(row+1), end="")
        
        print("\n" + "└──" + ("┴──" * (7)) + "┘")
        print(" a  b  c  d  e  f  g  h")
        
        print("Score: {} to {}".format(self.calculate_piece_totals()['W'], self.calculate_piece_totals()['B']))
        print(f"Score according to AI: {self.ai[0].score_board(self.board)}")

    def decode_move(self, move):
        if len(move) != 2:
            return False
        
        charx = move[0]
        chary = move[1]
        try:
            charx = ord(charx) - 97
            chary = int(chary) - 1
        except:
            return False

        return (chary, charx)

    def query_for_valid_move(self, char):
        print("Looks like it is {}'s turn!".format(char))
        valid_moves = self.calculate_valid_moves(char)
        if len(valid_moves) == 0:
            print("There are no moves available for them :(")
            return None

        self.print_self(valid_moves)
        move = self.decode_move(input("Enter the coordinate of the move you would like to make (ex. a2): "))

        while True:
            if move not in valid_moves:
                move = self.decode_move(input("That is not a valid move, please try again: "))
            else:
                break
        
        return move
    
    def query_ai_for_move(self, char, index):
        return self.ai[index].get_ideal_move(char, self.calculate_valid_moves(char), self.board)
    
    def calculate_piece_totals(self):
        totals = {'W': 0, 'B': 0}
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == self.whitechar:
                    totals['W'] += 1
                elif self.board[row][col] == self.blackchar:
                    totals['B'] += 1
        return totals

    def make_move(self, char, move):
        if move == None:
            return False

        try:
            row, col = move
        except TypeError:
            print(f"[Caught TypeError] That's not a valid move. Moves should be a structured tuple in this format (int, int). Each int must be [0,7].\nError unpacking ints from passed move: {move}")
            if move == -1:
                print("The move is -1, which is often used as an AI error code. This error code should never be passed to the Board class.\n")
            raise TypeError
        self.board[row][col] = char

        for row_dir in range(-1, 2):
            for col_dir in range(-1, 2):
                if row_dir == 0 and col_dir == 0:
                    continue
                if self.__is_dir_valid_to_convert(char, row, col, row_dir, col_dir, 0):
                    self.__convert_enemy_pieces_in_dir(char, row, col, row_dir, col_dir, 0)

        return True
                    
    def get_piece(self, row, col):
        return self.board[row][col]
    
    def set_piece(self, row, col, piece):
        self.board[row][col] = piece
    
    def get_board(self):
        return self.board
    
    # completes a move for the given direction
    def __is_dir_valid_to_convert(self, char, row, col, row_dir, col_dir, distance):
        if row < 0 or row > 7 or col < 0 or col > 7:
            return False
        
        if self.board[row][col] == char and distance > 0:
            return True
        
        if self.board[row][col] == '-':
            return False
        
        return self.__is_dir_valid_to_convert(char, row + row_dir, col + col_dir, row_dir, col_dir, distance + 1)
    
    def __convert_enemy_pieces_in_dir(self, char, row, col, row_dir, col_dir, distance):
        if self.board[row][col] == char and distance > 0:
            return
        
        if self.board[row][col] != '-' and self.board[row][col] != char:
            self.board[row][col] = char
        
        return self.__convert_enemy_pieces_in_dir(char, row + row_dir, col + col_dir, row_dir, col_dir, distance + 1)
    
    # checks if a move is valid in a given direction
    def __check_in_dir(self, char, row, col, row_dir, col_dir, d, found_enemy):
        # if we reached the end of the board return false
        if row < 0 or row > 7 or col < 0 or col > 7:
            return False
        
        # if we found an enemy piece return true
        if self.board[row][col] != char and self.board[row][col] != '-':
            found_enemy = True

        # if we found an enemy piece in between the start and our piece return true
        if self.board[row][col] == char and found_enemy:
            return True

        # if we found another of our piece and we haven't found an enemy piece yet return false
        elif self.board[row][col] == char:
            return False

        # if we found an empty space before we found our piece return false
        if self.board[row][col] == '-' and d != 0:
            return False

        # keep propagating in the direction we are going
        return self.__check_in_dir(char, row + row_dir, col + col_dir, row_dir, col_dir, d + 1, found_enemy)

    def calculate_valid_moves(self, char):
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col] != '-':
                    continue
                
                for row_dir in range(-1, 2):
                    for col_dir in range(-1, 2):
                        if row_dir == 0 and col_dir == 0:
                            continue
                        if self.__check_in_dir(char, row, col, row_dir, col_dir, 0, False):
                            valid_moves.append((row, col))
                            break
                    
        return valid_moves
    
    def count_pieces(self):
        pieces = 0
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == self.whitechar:
                    pieces += 1
                elif self.board[row][col] == self.blackchar:
                    pieces += 1
        
        return pieces
    
    def count_pieces_by_color(self):
        totals = {'W': 0, 'B': 0}
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == self.whitechar:
                    totals['W'] += 1
                elif self.board[row][col] == self.blackchar:
                    totals['B'] += 1
        
        return totals

def run_ai_vs_player():
    board = Board()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    ai = Minimax_AI() 
    board.ai = [ai]

    while True:
        skips = 0
        turn = 0
        os.system('clear')
        if board.make_move(board.whitechar, board.query_for_valid_move(board.whitechar)) == False:
            skips += 1

        os.system('clear')
        if board.calculate_valid_moves(board.blackchar) == []:
            print("Looks like it is B's turn!")
            board.print_self()
            print("Looks like the AI has no moves available!")
            time.sleep(2.5)
            skips += 1
        else:
            print(f"calculating {len(board.calculate_valid_moves(board.blackchar))} moves...")
            board.print_self()

            move = board.query_ai_for_move(board.blackchar, 0)
            
            os.system('clear')
            print(f"Looks like it is B's turn!")
            board.print_self([move])
            print("AI chose to place a piece at the 0.")
            board.last_ai_move = move
            time.sleep(2.5)
            board.make_move(board.blackchar, move)
        
        turn += 1

        if skips == 2:
            break

    os.system('clear')
    print("The game is over!")
    board.print_self()

if __name__ == "__main__":
    run_ai_vs_player()
