import numpy as np
import copy
from UI import UI
from Ai_Algorithms import AiAlgorithms
# game_board = [
#     ['o', None, None],
#     [None, 'x', 'o'],
#     [None, None, None],
# ]


def one_move_heuristic(board, ai_symbol):
    all_moves = all_possible_moves(board)
    best_move = all_moves[0]
    best_h = 10
    for move in all_moves:
        h = 0
        temp_board = copy.deepcopy(board)
        temp_board[move['row']][move['col']] = ai_symbol
        if is_game_over(temp_board)[0]:
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


def all_possible_moves(board):
    # all_possible_moves[{row:1,col:3},]
    all_moves = []
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                all_moves.append({'row': row, 'col': col})
    return all_moves


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


def symmetry_reduction(board):
    all_moves = []
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                move = {'row': row, 'col': col}
                if is_unique(move, all_moves, board):
                    all_moves.append(move)
    return all_moves


def minimax(board, depth, is_max, ai_symbol):
    best_move = {'row': -1, 'col': -1}
    is_over, result = is_game_over(board)
    if is_over:
        return best_move, 0 if result == 'tie' else 10 - depth if ai_symbol == result else depth - 10

    if is_max:
        best_score = -20
        for move in all_possible_moves(board):
            board[move['row']][move['col']] = ai_symbol
            rec_move, rec_result = minimax(board, depth + 1, False, ai_symbol)
            board[move['row']][move['col']] = None
            if rec_result > best_score:
                best_score = rec_result
                # using dict for shallow copy
                best_move = dict(move)
    else:
        best_score = 20
        for move in all_possible_moves(board):
            # all_possible_moves[{row:1,col:3},]
            board[move['row']][move['col']] = 'o' if ai_symbol == 'x' else 'x'
            rec_move, rec_result = minimax(board, depth + 1, True, ai_symbol)
            board[move['row']][move['col']] = None
            if rec_result < best_score:
                best_score = rec_result
                # using dict for shallow copy
                best_move = dict(move)
    return best_move, best_score


def alpha_beta(board, depth, alpha, beta, is_max, ai_symbol):
    best_move = {'row': -1, 'col': -1}
    is_over, result = is_game_over(board)
    if is_over:
        return best_move, 0 if result == 'tie' else 10 - depth if ai_symbol == result else depth - 10

    if is_max:
        best_score = -20
        for move in all_possible_moves(board):
            board[move['row']][move['col']] = ai_symbol
            rec_move, rec_result = alpha_beta(board, depth + 1, alpha, beta, False, ai_symbol)
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
        for move in all_possible_moves(board):
            # all_possible_moves[{row:1,col:3},]
            board[move['row']][move['col']] = 'o' if ai_symbol == 'x' else 'x'
            rec_move, rec_result = alpha_beta(board, depth + 1, alpha, beta, True, ai_symbol)
            board[move['row']][move['col']] = None
            beta = min(beta, rec_result)
            if rec_result < best_score:
                best_score = rec_result
                best_move = dict(move)

            if beta <= alpha:
                break
    return best_move, best_score


#######################################################


def update_board(board, position, symbol):
    # Convert position (1-9) into row and column
    try:
        row = (int(position) - 1) // 3
        col = (int(position) - 1) % 3

        # Update the board if the cell is empty
        if board[row][col] is None:
            board[row][col] = symbol
            return True
        else:
            print("Cell already occupied!")
            return False
    except:
        print('invalid move')
        return False


def print_board(board):
    count = 1
    for row in board:
        print(' | '.join(
            cell if cell is not None else str(count) for cell, count in zip(row, range(count, count + len(row)))))
        count += len(row)


if __name__ == "__main__":
    game = UI()

    game_board = [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]
    turn = 'x'
    print_board(game_board)
    game_over = is_game_over(game_board)
    while not game_over[0]:
        if turn == 'x':
            user = input('Choose number from 1 to 9: ')
            is_valid = update_board(game_board, user, 'x')
            if is_valid:
                turn = 'o'
            else:
                print_board(game_board)
        else:
            ai = AiAlgorithms()
            # comp_choice = one_move_heuristic(game_board, 'o')[0]
            comp_choice = ai.minimax(game_board, 0, True, 'o')[0]
            # comp_choice = alpha_beta(game_board, 0, -20, 20, True, 'o')[0]
            game_board[comp_choice['row']][comp_choice['col']] = 'o'
            turn = 'x'
            print_board(game_board)
        game_over = is_game_over(game_board)
        if game_over[0]:
            print(f'{game_over[1]} wins' if game_over[1] != 'tie' else 'tie')

