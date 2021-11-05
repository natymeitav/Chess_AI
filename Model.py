import copy

class CPU:

    @staticmethod
    def getBoards(logic,pieces):
        boards = []
        for piece in pieces:
            if piece is not None:
                print(str(piece)+str(piece.getMoves(logic)))

    # input: the captured piece
    # removes the piece from pieces array
    @staticmethod
    def unpersonPiece(black, white, casualty):
        if casualty.isWhite:
            white[casualty.serialNum] = None
        else:
            black[casualty.serialNum] = None

    @staticmethod
    def aaaa(logic,black,white):
        CPU.getBoards(logic,black)

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


