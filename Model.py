import copy


class CPU:

    @staticmethod
    def getBoards(logic, pieces):
        boards = []
        for piece in pieces:
            if piece is not None:
                for move in piece.getMoves(logic):
                    temp_logic = copy.deepcopy(logic)
                    temp_piece = copy.deepcopy(piece)

                    # update boards
                    temp_logic[move[0], move[1]] = temp_piece
                    temp_logic[temp_piece.pos[0], temp_piece.pos[1]] = None

                    # update piece's first move
                    if temp_logic[move[0], move[1]].firstMove:
                        temp_logic[move[0], move[1]].firstMove = False

                    # update piece's position
                    temp_logic[move[0], move[1]].pos = move

                    boards.append((temp_logic,temp_logic[move[0], move[1]].pos))

        return boards

    # TODO:
    # update captured pieces
    # fix MakeMove

    @staticmethod
    def MakeMove(logic, black, white):
        max_val = float('-inf')
        max_board = None
        max_piece = None
        for board in CPU.getBoards(logic, black):
            print("a")
            value = CPU.getMin(board[0], black, white, 1)
            if value > max_val:
                max_val = value
                max_board = board
                max_piece = board[1]

        return max_board, max_piece


    @staticmethod
    def getMax(logic, black, white, depth):

        if depth == 3:
            return 0

        max_val = float('-inf')

        endgame = CPU.checkEndGame(black,white)
        if endgame != -999:
            print("endgame "+ str(endgame))
            return endgame

        for board in CPU.getBoards(logic, black):
            value = CPU.getMin(board[0], black, white, depth+1)
            if value > max_val:
                max_val = value
        return max_val

    @staticmethod
    def getMin(logic, black, white, depth):

        if depth == 3:
            return 0

        min_val = float('inf')
        endgame = CPU.checkEndGame(black, white)
        if endgame != -999:
            print("endgame " + str(endgame))
            return endgame
        for board in CPU.getBoards(logic,white):
            board = board[0]
            value = CPU.getMax(board[0], black, white, depth+1)
            if value < min_val:
                min_val = value
        return min_val


    # check for win or tie
    @staticmethod
    def checkEndGame(black,white):
        # check for white win
        endgame = -999
        if str(black[4]) != "K0":
            endgame = 1
        # check for black win
        elif str(white[12]) != "K1":
            endgame = -1
        # check for insufficient material
        elif len(set(white + black)) == 3:
            endgame = 0

        return endgame

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
