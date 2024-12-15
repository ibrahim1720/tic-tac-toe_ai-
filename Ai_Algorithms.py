import copy
import numpy as np


class AiAlgorithms:

    @staticmethod
    def all_possible_moves(board):
        # all_possible_moves[{row:1,col:3},]
        all_moves = []
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    all_moves.append({'row': row, 'col': col})
        return all_moves

    @staticmethod
    def is_unique(move, moves, board):
        temp_board = copy.deepcopy(board)
        temp_board[move['row']][move['col']] = 'X'
        for i in range(1, 4):
            rotated_board = np.rot90(temp_board, k=i)
            rotated_move = {
                'row': np.where(rotated_board == 'X')[0][0],
                'col': np.where(rotated_board == 'X')[1][0]
            }

            if rotated_move in moves:
                old_board = copy.deepcopy(board)
                old_board[rotated_move['row']][rotated_move['col']] = 'X'
                if rotated_board.tolist() == old_board:
                    return False
        return True

    def symmetry_reduction(self, board):
        all_moves = []
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    move = {'row': row, 'col': col}
                    if self.is_unique(move, all_moves, board):
                        all_moves.append(move)
        return all_moves

    @staticmethod
    def is_game_over(board):
        # check rows
        for row in board:
            if row[0] is not None and row[0] == row[1] == row[2]:
                return True, row[0]
        # check cols
        for i in range(3):
            if board[0][i] is not None and board[0][i] == board[1][i] == board[2][i]:
                return True, board[0][i]
        # check diagonals
        if board[0][0] is not None and board[0][0] == board[1][1] == board[2][2]:
            return True, board[0][0]

        if board[0][2] is not None and board[0][2] == board[1][1] == board[2][0]:
            return True, board[0][2]

        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    return False, None

        return True, 'tie'

    def one_move_heuristic(self, board, ai_symbol):
        all_moves = self.all_possible_moves(board)
        best_move = all_moves[0]
        best_h = 10
        for move in all_moves:
            h = 0
            temp_board = copy.deepcopy(board)
            temp_board[move['row']][move['col']] = ai_symbol
            if self.is_game_over(temp_board)[0]:
                return move, 0
            else:
                # row
                for row in temp_board:
                    h = 0
                    for cell in row:
                        if cell is None:
                            h += 1
                        elif cell != ai_symbol:
                            h = 0
                            break
                    else:
                        if h < best_h:
                            best_h = h
                            best_move = move
                # col
                for i in range(3):
                    h = 0
                    for j in range(3):
                        if temp_board[j][i] is None:
                            h += 1
                        elif temp_board[j][i] is not ai_symbol:
                            h = 0
                            break
                    else:
                        if h < best_h:
                            best_h = h
                            best_move = move
                # diagonals
                for i in range(3):
                    if temp_board[i][i] is None:
                        h += 1
                    elif temp_board[i][i] is not ai_symbol:
                        break
                else:
                    if h < best_h:
                        best_h = h
                        best_move = move
                # another diagonal
                anti_diagonal = [(0, 2), (1, 1), (2, 0)]
                for i, j in anti_diagonal:
                    if temp_board[i][j] is None:
                        h += 1
                    elif temp_board[i][j] != ai_symbol:
                        break
                else:
                    if h < best_h:
                        best_h = h
                        best_move = move
        return best_move, 0

    def minimax(self, board, is_max, ai_symbol):
        best_move = {'row': -1, 'col': -1}
        is_over, result = self.is_game_over(board)
        if is_over:
            return best_move, 0 if result == 'tie' else 1 if ai_symbol == result else -1

        if is_max:
            best_score = -2
            for move in self.all_possible_moves(board):
                board[move['row']][move['col']] = ai_symbol
                rec_move, rec_result = self.minimax(board, False, ai_symbol)
                board[move['row']][move['col']] = None
                if rec_result > best_score:
                    best_score = rec_result
                    # using dict for shallow copy
                    best_move = dict(move)
        else:
            best_score = 2
            for move in self.all_possible_moves(board):
                # all_possible_moves[{row:1,col:3},]
                board[move['row']][move['col']] = 'o' if ai_symbol == 'x' else 'x'
                rec_move, rec_result = self.minimax(board, True, ai_symbol)
                board[move['row']][move['col']] = None
                if rec_result < best_score:
                    best_score = rec_result
                    # using dict for shallow copy
                    best_move = dict(move)
        return best_move, best_score

    def minimax_depth(self, board, depth, is_max, ai_symbol):
        best_move = {'row': -1, 'col': -1}
        is_over, result = self.is_game_over(board)
        if is_over:
            return best_move, 0 if result == 'tie' else 10 - depth if ai_symbol == result else depth - 10

        if is_max:
            best_score = -20
            for move in self.all_possible_moves(board):
                board[move['row']][move['col']] = ai_symbol
                rec_move, rec_result = self.minimax_depth(board, depth + 1, False, ai_symbol)
                board[move['row']][move['col']] = None
                if rec_result > best_score:
                    best_score = rec_result
                    # using dict for shallow copy
                    best_move = dict(move)
        else:
            best_score = 20
            for move in self.all_possible_moves(board):
                # all_possible_moves[{row:1,col:3},]
                board[move['row']][move['col']] = 'o' if ai_symbol == 'x' else 'x'
                rec_move, rec_result = self.minimax_depth(board, depth + 1, True, ai_symbol)
                board[move['row']][move['col']] = None
                if rec_result < best_score:
                    best_score = rec_result
                    # using dict for shallow copy
                    best_move = dict(move)
        return best_move, best_score

    def alpha_beta(self, board, alpha, beta, is_max, ai_symbol):
        best_move = {'row': -1, 'col': -1}
        is_over, result = self.is_game_over(board)
        if is_over:
            return best_move, 0 if result == 'tie' else 1 if ai_symbol == result else -1

        if is_max:
            best_score = -2
            for move in self.all_possible_moves(board):
                board[move['row']][move['col']] = ai_symbol
                rec_move, rec_result = self.alpha_beta(board, alpha, beta, False, ai_symbol)
                board[move['row']][move['col']] = None
                alpha = max(alpha, rec_result)
                if rec_result > best_score:
                    best_score = rec_result
                    # using dict for shallow copy
                    best_move = dict(move)

                if beta <= alpha:
                    break
        else:
            best_score = 2
            for move in self.all_possible_moves(board):
                # all_possible_moves[{row:1,col:3},]
                board[move['row']][move['col']] = 'o' if ai_symbol == 'x' else 'x'
                rec_move, rec_result = self.alpha_beta(board, alpha, beta, True, ai_symbol)
                board[move['row']][move['col']] = None
                beta = min(beta, rec_result)
                if rec_result < best_score:
                    best_score = rec_result
                    best_move = dict(move)

                if beta <= alpha:
                    break
        return best_move, best_score

    def alpha_beta_depth(self, board, depth, alpha, beta, is_max, ai_symbol):
        best_move = {'row': -1, 'col': -1}
        is_over, result = self.is_game_over(board)
        if is_over:
            return best_move, 0 if result == 'tie' else 10 - depth if ai_symbol == result else depth - 10

        if is_max:
            best_score = -20
            for move in self.all_possible_moves(board):
                board[move['row']][move['col']] = ai_symbol
                rec_move, rec_result = self.alpha_beta_depth(board, depth + 1, alpha, beta, False, ai_symbol)
                board[move['row']][move['col']] = None
                alpha = max(alpha, rec_result)
                if rec_result > best_score:
                    best_score = rec_result
                    # using dict for shallow copy
                    best_move = dict(move)

                if beta <= alpha:
                    break
        else:
            best_score = 20
            for move in self.all_possible_moves(board):
                # all_possible_moves[{row:1,col:3},]
                board[move['row']][move['col']] = 'o' if ai_symbol == 'x' else 'x'
                rec_move, rec_result = self.alpha_beta_depth(board, depth + 1, alpha, beta, True, ai_symbol)
                board[move['row']][move['col']] = None
                beta = min(beta, rec_result)
                if rec_result < best_score:
                    best_score = rec_result
                    best_move = dict(move)

                if beta <= alpha:
                    break
        return best_move, best_score

    def alpha_beta_symmetry(self, board, depth, alpha, beta, is_max, ai_symbol):
        best_move = {'row': -1, 'col': -1}
        is_over, result = self.is_game_over(board)
        if is_over:
            return best_move, 0 if result == 'tie' else 10 - depth if ai_symbol == result else depth - 10

        if is_max:
            best_score = -20
            for move in self.symmetry_reduction(board):
                board[move['row']][move['col']] = ai_symbol
                rec_move, rec_result = self.alpha_beta_symmetry(board, depth + 1, alpha, beta, False, ai_symbol)
                board[move['row']][move['col']] = None
                alpha = max(alpha, rec_result)
                if rec_result > best_score:
                    best_score = rec_result
                    # using dict for shallow copy
                    best_move = dict(move)

                if beta <= alpha:
                    break
        else:
            best_score = 20
            for move in self.symmetry_reduction(board):
                # all_possible_moves[{row:1,col:3},]
                board[move['row']][move['col']] = 'o' if ai_symbol == 'x' else 'x'
                rec_move, rec_result = self.alpha_beta_symmetry(board, depth + 1, alpha, beta, True, ai_symbol)
                board[move['row']][move['col']] = None
                beta = min(beta, rec_result)
                if rec_result < best_score:
                    best_score = rec_result
                    best_move = dict(move)

                if beta <= alpha:
                    break
        return best_move, best_score

    def minimax_heuristic_reduction(self, board, depth, is_max, ai_symbol):
        best_move = {'row': -1, 'col': -1}
        is_over, result = self.is_game_over(board)
        if is_over:
            return best_move, 0 if result == 'tie' else 10 - depth if ai_symbol == result else depth - 10
        all_moves = self.all_possible_moves(board)
        # checking first move
        if len(all_moves) >= 8:
            if board[1][1] is None:
                return {'row': 1, 'col': 1}, 0
            else:
                return {'row': 0, 'col': 0}, 0
        if is_max:
            best_score = -20
            for move in all_moves:
                board[move['row']][move['col']] = ai_symbol
                rec_move, rec_result = self.minimax_heuristic_reduction(board, depth + 1, False, ai_symbol)
                board[move['row']][move['col']] = None
                if rec_result > best_score:
                    best_score = rec_result
                    # using dict for shallow copy
                    best_move = dict(move)
        else:
            best_score = 20
            for move in all_moves:
                # all_possible_moves[{row:1,col:3},]
                board[move['row']][move['col']] = 'o' if ai_symbol == 'x' else 'x'
                rec_move, rec_result = self.minimax_heuristic_reduction(board, depth + 1, True, ai_symbol)
                board[move['row']][move['col']] = None
                if rec_result < best_score:
                    best_score = rec_result
                    # using dict for shallow copy
                    best_move = dict(move)
        return best_move, best_score
