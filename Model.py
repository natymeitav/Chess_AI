import copy


class CPU:

    @staticmethod
    def getBoards(logic, pieces):
        boards = []
        for piece in pieces:
            if piece is not None:
                for move in piece.getMoves(logic):
                    temp = copy.deepcopy(logic)

                    temp[move[0],move[1]] = piece
                    temp[piece.pos[0],piece.pos[1]] = None

                    boards.append(temp)

        return boards


    @staticmethod
    def MakeMove(logic, black, white):
        for board in CPU.getBoards(logic,black):
            CPU.printBoard(board)

    # input: the captured piece
    # removes the piece from pieces array
    @staticmethod
    def unpersonPiece(black, white, casualty):
        if casualty.isWhite:
            white[casualty.serialNum] = None
        else:
            black[casualty.serialNum] = None

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
