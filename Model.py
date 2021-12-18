import copy


class CPU:

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
                    temp_logic[move[0], move[1]] = temp_piece
                    temp_logic[temp_piece.pos[0], temp_piece.pos[1]] = None

                    # update piece's first move
                    if temp_logic[move[0], move[1]].firstMove:
                        temp_logic[move[0], move[1]].firstMove = False

                    # update piece's position
                    temp_logic[move[0], move[1]].pos = move

                    boards.append([temp_logic, [piece_pos, (move[0], move[1])]])

        return boards

    # find best next move
    @staticmethod
    def makeMove(logic, black, white):

        # setup max values
        max_val = float('-inf')
        max_piece = None

        # find best move for black
        for board in CPU.getBoards(logic, black):

            # copy black and white pieces
            temp_black = copy.deepcopy(black)
            temp_white = copy.deepcopy(white)

            if CPU.checkTie(temp_black, temp_white):
                print("tie")
                return 0

            piece_pos = board[1][1]

            # check for capture
            if logic[piece_pos[0], piece_pos[1]] is not None:
                temp_black, temp_white = CPU.deletePiece(temp_black, temp_white, logic[piece_pos[0], piece_pos[1]])

            value = CPU.getMin(board[0], temp_black, temp_white, 1) + CPU.evaluation_val(black,white)
            print(value)
            if value > max_val:
                max_val = value
                max_piece = board[1]
        return max_piece

    @staticmethod
    def getMax(logic, black, white, depth):
        # check for max depth
        if depth == 3:
            return CPU.evaluation_val(black,white)

        # setup max values
        max_val = float('-inf')

        # find best move for black
        for board in CPU.getBoards(logic, black):

            # copy black and white pieces
            temp_black = copy.deepcopy(black)
            temp_white = copy.deepcopy(white)

            if CPU.checkTie(temp_black, temp_white):
                print("tie")
                return 0

            piece_pos = board[1][1]

            # check for capture
            if logic[piece_pos[0], piece_pos[1]] is not None:
                black, white = CPU.deletePiece(temp_black, temp_white, logic[piece_pos[0], piece_pos[1]])

            value = CPU.getMin(board[0], temp_black, temp_white, depth + 1) + CPU.evaluation_val(black,white)
            if value > max_val:
                max_val = value

        return max_val

    @staticmethod
    def getMin(logic, black, white, depth):

        # check for max depth
        if depth == 3:
            return CPU.evaluation_val(black,white)

        # setup mon values
        min_val = float('inf')

        # find worst move for black
        for board in CPU.getBoards(logic, white):

            # copy black and white pieces
            temp_black = copy.deepcopy(black)
            temp_white = copy.deepcopy(white)

            if CPU.checkTie(temp_black, temp_white):
                print("tie")
                return 0

            piece_pos = board[1][1]

            # check for capture
            if logic[piece_pos[0], piece_pos[1]] is not None:
                temp_black, temp_white = CPU.deletePiece(temp_black, temp_white, logic[piece_pos[0], piece_pos[1]])

            value = CPU.getMax(board[0], temp_black, temp_white, depth + 1) + CPU.evaluation_val(black,white)
            if value < min_val:
                min_val = value

        return min_val

    @staticmethod
    def deletePiece(black, white, captured):
        if captured.isWhite:
            white[captured.serialNum] = None
        else:
            black[captured.serialNum] = None
        return black, white

    @staticmethod
    def evaluation_val(black,white):
        sum = 0
        pieces = black + white
        for piece in pieces:
            if piece is not None:
                sum += piece.value
        return sum

    # check for tie
    @staticmethod
    def checkTie(black, white):
        return len(set(white + black)) == 3

    @staticmethod
    def printBoard(listLogicBoard):
        for row in range(len(listLogicBoard)):
            print("")
            for col in range(len(listLogicBoard)):
                square = listLogicBoard[row, col]
                if square is None:
                    print("--", end=" ")
                else:
                    print(square, end=" ")
        print("")

    @staticmethod
    def printLine(line):
        for row in range(len(line)):
            square = line[row]
            if square is None:
                print("--", end=" ")
            else:
                print(square, end=" ")
        print("")
