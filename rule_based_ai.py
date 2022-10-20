import copy

class Rule_AI:
    def __init__(self):
        self.value_matrix = [[ 3, -2,  2,  0,  0,  2, -2,  3],
                             [-2, -2, -1,  0,  0, -1, -2, -2],
                             [ 2, -1,  1,  1,  1,  1, -1,  2],
                             [ 0,  0,  1,  1,  1,  1,  0,  0],
                             [ 0,  0,  1,  1,  1,  1,  0,  0],
                             [ 2, -1,  1,  1,  1,  1, -1,  2],
                             [-2, -2, -1,  0,  0, -1, -2, -2],
                             [ 3, -2,  2,  0,  0,  2, -2,  3]]
    
    def get_value_matrix(self, board, char):
        new_matrix = copy.deepcopy(self.value_matrix)

        if board[0][2] == char and board[0][5] == char:
            new_matrix[0][3] = new_matrix[0][4] = 1
        if board[2][0] == char and board[5][0] == char:
            new_matrix[3][0] = new_matrix[4][0] = 1
        if board[7][2] == char and board[7][5] == char:
            new_matrix[7][3] = new_matrix[7][4] = 1
        if board[2][7] == char and board[5][7] == char:
            new_matrix[3][7] = new_matrix[4][7] = 1
        
        return new_matrix

    def get_ideal_move(self, char : str, valid_moves : list, board):
        if len(valid_moves) == 0:
            return None
        
        values = self.get_corresponding_values(valid_moves, board, char)
        max_value = max(values)
        max_index = values.index(max_value)

        return valid_moves[max_index]

    def get_value(self, move : tuple, board, char):
        try:
            row, col = move
        except TypeError:
            return None

        return self.get_value_matrix(board, char)[row][col]

    def get_corresponding_values(self, moves : list, board, char):
        values = []
        for move in moves:
            values.append(self.get_value(move, board, char))
        return values
