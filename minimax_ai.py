import copy
import time
import random

class Minimax_AI:
    def __init__(self, whitechar = 'W', blackchar = 'B'):
        self.whitechar = whitechar
        self.blackchar = blackchar
        self.our_color = self.blackchar
        self.pieces_remaining = 0

        self.early_matrix = [[ 3, -2,  2,  0,  0,  2, -2,  3],
                             [-2, -2, -1,  0,  0, -1, -2, -2],
                             [ 2, -1,  1,  1,  1,  1, -1,  2],
                             [ 0,  0,  1,  1,  1,  1,  0,  0],
                             [ 0,  0,  1,  1,  1,  1,  0,  0],
                             [ 2, -1,  1,  1,  1,  1, -1,  2],
                             [-2, -2, -1,  0,  0, -1, -2, -2],
                             [ 3, -2,  2,  0,  0,  2, -2,  3]]
        
        self.eamid_matrix = [[ 3, -2,  2,  0,  0,  2, -2,  3],
                             [-2, -2, -1,  0,  0, -1, -2, -2],
                             [ 2, -1,  1,  1,  1,  1, -1,  2],
                             [ 0,  0,  1,  1,  1,  1,  0,  0],
                             [ 0,  0,  1,  1,  1,  1,  0,  0],
                             [ 2, -1,  1,  1,  1,  1, -1,  2],
                             [-2, -2, -1,  0,  0, -1, -2, -2],
                             [ 3, -2,  2,  0,  0,  2, -2,  3]]

        self.lamid_matrix = [[ 3, -2,  2,  0,  0,  2, -2,  3],
                             [-2, -2, -1,  0,  0, -1, -2, -2],
                             [ 2, -1,  1,  1,  1,  1, -1,  2],
                             [ 0,  0,  1,  1,  1,  1,  0,  0],
                             [ 0,  0,  1,  1,  1,  1,  0,  0],
                             [ 2, -1,  1,  1,  1,  1, -1,  2],
                             [-2, -2, -1,  0,  0, -1, -2, -2],
                             [ 3, -2,  2,  0,  0,  2, -2,  3]]
    
    def mutate_core(self):
        for i in range(10):
            table = random.randint(1, 2)
            if table == 1:
                row = random.randint(0, 7)
                col = random.randint(0, 7)
                self.eamid_matrix[row][col] += random.randint(-1, 1)
            elif table == 2:
                row = random.randint(0, 7)
                col = random.randint(0, 7)
                self.lamid_matrix[row][col] += random.randint(-1, 1)

    def visualize_core(self):
        for row in range(8):
            for col in range(8):
                if(self.early_matrix[row][col] >= 0):
                    print(' ' + str(self.early_matrix[row][col]), end = ' ')
                else:
                    print(self.early_matrix[row][col], end = ' ')
            print()
        print()

        for row in range(8):
            for col in range(8):
                if(self.eamid_matrix[row][col] >= 0):
                    print(' ' + str(self.eamid_matrix[row][col]), end = ' ')
                else:
                    print(self.eamid_matrix[row][col], end = ' ')
            print()
        print()

        for row in range(8):
            for col in range(8):
                if(self.lamid_matrix[row][col] >= 0):
                    print(' ' + str(self.lamid_matrix[row][col]), end = ' ')
                else:
                    print(self.lamid_matrix[row][col], end = ' ')
            print()
        print()

    def dump_core_to_file(self):
        core = open('core.txt', 'w')
        core.write(str(self.early_matrix) + '\n')
        core.write(str(self.eamid_matrix) + '\n')
        core.write(str(self.lamid_matrix) + '\n')
        core.close()

    def import_core_from_file(self):
        core = open('core.txt', 'r')
        self.early_matrix = eval(core.readline())
        self.eamid_matrix = eval(core.readline())
        self.lamid_matrix = eval(core.readline())
        core.close()

    def score_board(self, board):
        score = 0
        # use value matrix to calculate score
        if self.pieces_remaining > 40:
            for row in range(8):
                for col in range(8):
                    if board[row][col] == self.whitechar:
                        score += self.early_matrix[row][col]
                    elif board[row][col] == self.blackchar:
                        score -= self.early_matrix[row][col]
        elif self.pieces_remaining > 30:
            for row in range(8):
                for col in range(8):
                    if board[row][col] == self.whitechar:
                        score += self.eamid_matrix[row][col]
                    elif board[row][col] == self.blackchar:
                        score -= self.eamid_matrix[row][col]
        elif self.pieces_remaining > 16:
            for row in range(8):
                for col in range(8):
                    if board[row][col] == self.whitechar:
                        score += self.lamid_matrix[row][col]
                    elif board[row][col] == self.blackchar:
                        score -= self.lamid_matrix[row][col]
        else:
            for row in range(8):
                for col in range(8):
                    if board[row][col] == self.whitechar:
                        score += self.lamid_matrix[row][col] / 2
                        score += 4
                    elif board[row][col] == self.blackchar:
                        score -= self.lamid_matrix[row][col] / 2
                        score -= 4
                    
        return score

    def count_pieces(self, board):
        pieces_remaining = 64
        for row in range(8):
            for col in range(8):
                if board[row][col] == self.whitechar or board[row][col] == self.blackchar:
                    pieces_remaining -= 1
        return pieces_remaining

    def get_ideal_move(self, char : str, valid_moves : list, board):
        self.complete = False
        self.pieces_remaining = self.count_pieces(board)

        if char == self.whitechar:
            self.our_color = self.whitechar
        else:
            self.our_color = self.blackchar

        if len(valid_moves) == 0:
            return None
        elif len(valid_moves) == 1:
            return valid_moves[0]

        best_move = None
        if char == self.whitechar:
            best_score = -99999
        else:
            best_score = 99999

        depth = 6
        
        progress = 0
        print("[", end="")
        total_prog = progress / len(valid_moves)
        bars = round(total_prog * 25)
        whitespace = 25 - bars

        print("=" * bars, end="")
        print(" " * whitespace, end="")
        print(f"] depth is {depth}.    ", end="\r")
        
        for move in valid_moves:
            start_time = time.time()
            new_board = self.copy_board(board)
            self.make_move(new_board, self.our_color, move)
            if char == self.whitechar:
                score = self.minimax(new_board, depth, -99999, 99999, False)
            else:
                score = self.minimax(new_board, depth, -999999, 99999, True)

            if char == self.whitechar:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
            
            if (time.time() - start_time) * len(valid_moves) > 15:
                depth -= 2
            elif (time.time() - start_time) * len(valid_moves) < 1.5 and depth >= 8:
                factor = (time.time() - start_time) * len(valid_moves) / 15
                if factor < 0.25:
                    depth += 4
                else:
                    depth += 2

            progress += 1

            print("[", end="")
            total_prog = progress / len(valid_moves)
            bars = round(total_prog * 25)
            whitespace = 25 - bars

            print("=" * bars, end="")
            print(" " * whitespace, end="")
            print(f"] depth is {depth}.    ", end="\r")  
        
        return best_move

    def copy_board(self, board):
        new_board = copy.deepcopy(board)
        return new_board

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        if depth == 0:
            return self.score_board(board)

        if is_maximizing:
            char = self.whitechar
        else:
            char = self.blackchar

        valid_moves = self.calculate_valid_moves(board, char)
        if len(valid_moves) == 0:
            return self.score_board(board)

        if is_maximizing:
            best_score = -999999
            for move in valid_moves:
                new_board = self.copy_board(board)
                self.make_move(new_board, char, move)
                score = self.minimax(new_board, depth - 1, alpha, beta, False)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = 99999
            for move in valid_moves:
                new_board = self.copy_board(board)
                self.make_move(new_board, char, move)
                score = self.minimax(new_board, depth - 1, alpha, beta, True)
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score

    def make_move(self, board, char, move):
        if move == None:
            return False

        row, col = move
        board[row][col] = char

        for row_dir in range(-1, 2):
            for col_dir in range(-1, 2):
                if row_dir == 0 and col_dir == 0:
                    continue
                if self.__is_dir_valid_to_convert(board, char, row, col, row_dir, col_dir, 0):
                    self.__convert_enemy_pieces_in_dir(board, char, row, col, row_dir, col_dir, 0)

        return True
    
    # completes a move for the given direction
    def __is_dir_valid_to_convert(self, board, char, row, col, row_dir, col_dir, distance):
        if row < 0 or row > 7 or col < 0 or col > 7:
            return False
        
        if board[row][col] == char and distance > 0:
            return True
        
        if board[row][col] == '-':
            return False
        
        return self.__is_dir_valid_to_convert(board, char, row + row_dir, col + col_dir, row_dir, col_dir, distance + 1)
    
    def __convert_enemy_pieces_in_dir(self, board, char, row, col, row_dir, col_dir, distance):
        if board[row][col] == char and distance > 0:
            return
        
        if board[row][col] != '-' and board[row][col] != char:
            board[row][col] = char
        
        return self.__convert_enemy_pieces_in_dir(board, char, row + row_dir, col + col_dir, row_dir, col_dir, distance + 1)
    
    # checks if a move is valid in a given direction
    def __check_in_dir(self, board, char, row, col, row_dir, col_dir, d, found_enemy):
        # if we reached the end of the board return false
        if row < 0 or row > 7 or col < 0 or col > 7:
            return False
        
        # if we found an enemy piece return true
        if board[row][col] != char and board[row][col] != '-':
            found_enemy = True

        # if we found an enemy piece in between the start and our piece return true
        if board[row][col] == char and found_enemy:
            return True

        # if we found another of our piece and we haven't found an enemy piece yet return false
        elif board[row][col] == char:
            return False

        # if we found an empty space before we found our piece return false
        if board[row][col] == '-' and d != 0:
            return False

        # keep propagating in the direction we are going
        return self.__check_in_dir(board, char, row + row_dir, col + col_dir, row_dir, col_dir, d + 1, found_enemy)

    def calculate_valid_moves(self, board, char):
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if board[row][col] != '-':
                    continue
                
                for row_dir in range(-1, 2):
                    for col_dir in range(-1, 2):
                        if row_dir == 0 and col_dir == 0:
                            continue
                        if self.__check_in_dir(board, char, row, col, row_dir, col_dir, 0, False):
                            valid_moves.append((row, col))
                            break
                    
        return valid_moves