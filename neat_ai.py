
import time

class Neat_AI_Wrapper:
    def __init__(self, core_nn):
        self.core_nn = core_nn
    
    def get_ideal_move(self, char : str, valid_moves : list, board):
        move = self.core_nn.activate(self.get_nn_inputs(char, board))[0]
        move = self.convert_nn_output(move, valid_moves)

        return move
    
    def score_board(self, board):
        return 0

    def convert_nn_output(self, output, valid_moves):
        output = output * 64
        output = round(output)
        row = output // 8
        col = output % 8
        move = (row, col)

        if move in valid_moves:
            return move
        else:
            # find valid move that is closest to the generated move
            best_distance = 64
            best_move = None

            for valid_move in valid_moves:
                distance = abs((move[0] - valid_move[0])) + abs((move[1] - valid_move[1]))

                if distance < best_distance:
                    best_distance = distance
                    best_move = valid_move
        
        return best_move
            
    
    def get_nn_inputs(self, char, board):
        inputs = []
        if char == 'W':
            inputs.append(1)
        else:
            inputs.append(0)

        for i in range(8):
            for j in range(8):
                if board[i][j] == '-':
                    inputs.append(0.5)
                elif board[i][j] == 'W':
                    inputs.append(1)
                elif board[i][j] == 'B':
                    inputs.append(0)

        return inputs