import copy


class Talos:

    # return array of posible moves [board,[position before, position after]]
    @staticmethod
    def getBoards(logic, pieces):
        boards = []
        for piece in pieces:
            if piece is not None:
                for move in piece.getMoves(logic):
                    temp_logic = copy.deepcopy(logic)
                    temp_piece = copy.deepcopy(piece)

                    piece_pos = piece.pos

                    # update boards
                    temp_logic[temp_piece.pos[0], temp_piece.pos[1]] = None
                    temp_logic[move[0], move[1]] = temp_piece

                    # update piece's first move
                    if temp_logic[move[0], move[1]].firstMove:
                        temp_logic[move[0], move[1]].firstMove = False

                        # check for castling
                        if piece.type == "K":
                            if move[1] == 2:
                                temp_logic = Talos.castle([move[0], 0], [move[0], 3],temp_logic)
                            elif move[1] == 6:
                                temp_logic = Talos.castle([move[0], 7], [move[0], 5],temp_logic)

                    # update piece's position
                    temp_logic[move[0], move[1]].pos = move

                    boards.append([temp_logic, [piece_pos, (move[0], move[1])]])

        return boards

    # moves rook while castling
    @staticmethod
    def castle(old_pos, new_pos, logic):
        piece = logic[old_pos[0], old_pos[1]]

        # update logic board
        logic[old_pos[0], old_pos[1]] = None
        logic[new_pos[0], new_pos[1]] = piece

        # update piece's first move
        logic[new_pos[0], new_pos[1]].firstMove = False

        # update piece's position
        piece.pos = new_pos

        return logic

    # find best next move
    @staticmethod
    def make_move(logic, black, white, depth):

        # setup values
        alpha = float('-inf')
        beta = float('inf')

        boards = Talos.ordering(Talos.getBoards(logic, black), black, white, logic, False)
        max_board = boards[0]
        max_val = float('-inf')

        # find best move for black
        for board in boards:
            # copy black and white pieces
            temp_black = copy.deepcopy(black)
            temp_white = copy.deepcopy(white)

            piece_pos = board[1][1]

            # check for capture
            if logic[piece_pos[0], piece_pos[1]] is not None:
                temp_black, temp_white = Talos.deletePiece(temp_black, temp_white,
                                                           logic[piece_pos[0], piece_pos[1]])

            if Talos.checkEndGame(temp_black, temp_white):
                value = Talos.checkEndGame(temp_black, temp_white)
            else:
                value = Talos.getMin(board[0], temp_black, temp_white, depth, alpha, beta)
                # print(piece_pos)

            if value > max_val:
                max_val = value
                max_board = board

                if alpha < max_val:
                    alpha = max_val
                    if beta <= alpha:
                        break

        print(str(max_board[1][1]) + " " + str(max_val))
        return max_board[1]

    # returns the value of the best move for the opponent
    @staticmethod
    def getMin(logic, black, white, depth, alpha, beta):

        # check for max depth
        if depth == 0:
            return Talos.evaluation_val(black, white, logic)

        # setup mon values
        min_val = float('inf')

        boards = Talos.ordering(Talos.getBoards(logic, white), white, black, logic, False)

        # find worst move for black
        for board in boards:

            # copy black and white pieces
            temp_black = copy.deepcopy(black)
            temp_white = copy.deepcopy(white)

            piece_pos = board[1][1]
            # check for capture
            if logic[piece_pos[0], piece_pos[1]] is not None:
                temp_black, temp_white = Talos.deletePiece(temp_black, temp_white, logic[piece_pos[0], piece_pos[1]])

            if Talos.checkEndGame(temp_black, temp_white):
                return Talos.checkEndGame(temp_black, temp_white)

            value = Talos.getMax(board[0], temp_black, temp_white, depth - 1, alpha, beta)

            if value < min_val:
                min_val = value
                if beta > min_val:
                    beta = min_val
                    if beta <= alpha:
                        break

        return min_val

    # return the value of best move for computer
    @staticmethod
    def getMax(logic, black, white, depth, alpha, beta):

        # check for max depth
        if depth == 0:
            return Talos.evaluation_val(black, white, logic)

        # setup mon values
        max_val = float('-inf')

        boards = Talos.ordering(Talos.getBoards(logic, black), black, white, logic, False)

        # find worst move for black
        for board in boards:

            # copy black and white pieces
            temp_black = copy.deepcopy(black)
            temp_white = copy.deepcopy(white)

            piece_pos = board[1][1]
            # check for capture
            if logic[piece_pos[0], piece_pos[1]] is not None:
                temp_black, temp_white = Talos.deletePiece(temp_black, temp_white, logic[piece_pos[0], piece_pos[1]])

            if Talos.checkEndGame(temp_black, temp_white):
                return Talos.checkEndGame(temp_black, temp_white)

            value = Talos.getMin(board[0], temp_black, temp_white, depth - 1, alpha, beta)

            if value > max_val:
                max_val = value

                if alpha < max_val:
                    alpha = max_val
                    if beta <= alpha:
                        break
        return max_val

    # replaces captured piece with None in piece lists (black & white)
    @staticmethod
    def deletePiece(black, white, captured):
        if captured.isWhite:
            white[captured.serialNum] = None
        else:
            black[captured.serialNum] = None
        return black, white

    # changes order of moves to find better boards faster
    @staticmethod
    def ordering(boards, allys, enemies, logic, isWhite):
        order = []
        if isWhite:
            black = copy.deepcopy(enemies)
            white = copy.deepcopy(allys)
        else:
            black = copy.deepcopy(allys)
            white = copy.deepcopy(enemies)

        for board in boards:
            index = -1

            piece_pos = board[1][1]
            # check for capture
            if logic[piece_pos[0], piece_pos[1]] is not None:
                index = 0

            # check for dangerous position
            for enemy in white:
                if enemy is not None:
                    if piece_pos in enemy.getMoves(board[0]):
                        if len(order) - 1 > index:
                            index += 1

            # check for protection
            for ally in black:
                if ally is not None:
                    if piece_pos in ally.getMoves(board[0]):
                        if 1 < index:
                            index -= 2
                        elif index == 1:
                            index = 0

            order.insert(index, board)

        return order

    # returns value of board
    @staticmethod
    def evaluation_val(black, white, logic):
        value_sum, space_sum, center_val = Talos.get_values(black, white, logic)
        saftey_val = Talos.safety_val(black, white, logic)
        return 0.9 * value_sum + 0.2 * space_sum + 0.3 * center_val - 0.7 * saftey_val

    # returns evaluation values
    @staticmethod
    def get_values(black, white, logic):
        sum = 0  # the sum of pieces on board
        moves_sum = 0  # the difference between black's possible moves and white's possible moves
        center_val = 0  # the sum of piece's center of control
        for piece in black:
            if piece is not None:
                sum += piece.value

                moves = piece.getMoves(logic)
                moves_sum += len(moves)

                # check center_control
                center_val += Talos.center_val(piece.pos, piece.value)

        for piece in white:
            if piece is not None:
                sum += piece.value

                moves = piece.getMoves(logic)
                moves_sum -= len(moves)

                # check center_control
                center_val += Talos.center_val(piece.pos, piece.value)

        return sum, moves_sum, center_val

    # returns piece's control over the center
    @staticmethod
    def center_val(pos, val):
        if 3 <= pos[0] <= 4 and 3 <= pos[1] <= 4:
            return val
        elif 2 <= pos[0] <= 5 and 2 <= pos[1] <= 5:
            return val * 0.8
        else:
            return 0

    # returns the difference between black king's safety to white king's safety
    @staticmethod
    def safety_val(black, white, logic):
        return len(black[4].getMoves(logic)) - len(white[12].getMoves(logic))

    # check for endgame
    @staticmethod
    def checkEndGame(black, white):
        # check for white win
        if str(black[4]) != "K0":
            return float('-inf')
        # check for black win
        elif str(white[12]) != "K1":
            return float('inf')
        # check for insufficient material
        elif len(set(white + black)) == 4:
            return 0
