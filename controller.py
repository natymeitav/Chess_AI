import numpy as np
import random
from pieces import King, Rook, Knight, Bishop, Queen, Pawn


class Controller:  # keeps the logic board and rules of the game
    def __init__(self, cols, parent):

        self.black = []  # black pieces
        self.white = []  # white pieces

        self.listLogicBoard = self.buildLogicBoard(cols)
        self.printBoard()
        self.whiteTurn = True
        self.parent = parent
        self.isGameOver = False

        self.CPU_player = True

    # input: the number of lines\cols
    # output: a logic board with every position set to 'empty'
    def buildLogicBoard(self, cols):
        board = np.full((cols, cols), None)
        pieces = ["R", "N", "B", "Q", "P"]  # [rook , knight, bishop , queen, pawn]
        serial = 0
        # add pieces to top lines
        for row in range(2):
            for col in range(len(board)):
                if row == 0 and col == 4:
                    piece = King.King(False, (row, col), serial)  # add black king
                else:
                    piece = self.createPiece(random.choice(pieces), False)  # add black piece
                    piece.pos = (row, col)
                    piece.serialNum = serial

                serial += 1
                self.black.append(piece)
                board[row, col] = piece

        serial = 0
        # add pieces to bottom lines
        for row in range(6, 8):
            for col in range(len(board)):
                if row == 7 and col == 4:
                    piece = King.King(True, (row, col),serial)  # add white king
                else:
                    piece = self.createPiece(random.choice(pieces), True)  # add white piece
                    piece.pos = (row, col)
                    piece.serialNum = serial

                serial += 1
                self.white.append(piece)
                board[row, col] = piece

        return board

    def createPiece(self, type, isWhite):
        if type == "R":
            return Rook.Rook(isWhite, (-999, -999), -999)
        if type == "N":
            return Knight.Knight(isWhite, (-999, -999), -999)
        if type == "B":
            return Bishop.Bishop(isWhite, (-999, -999), -999)
        if type == "Q":
            return Queen.Queen(isWhite, (-999, -999), -999)
        if type == "P":
            return Pawn.Pawn(isWhite, (-999, -999), -999)

    # input: piece's position and new pos
    # returns if the move made is legal
    def isLegal(self, old, new):
        # is white moves on white's turn or is black moving on black's turn
        old_legal = self.listLogicBoard[old[0], old[1]].isWhite == self.whiteTurn
        if self.listLogicBoard[new[0], new[1]] is not None:
            new_legal = self.listLogicBoard[old[0], old[1]].isWhite != self.listLogicBoard[new[0], new[1]].isWhite
        else:
            new_legal = True
        move_legal = self.listLogicBoard[old[0], old[1]].canMakeMove(new,
                                                                     self.listLogicBoard)  # can piece move between old and new positions

        return old_legal and new_legal and move_legal

    # update controller and view to reflect move made
    def logMove(self, old_pos, new_pos):
        piece = self.listLogicBoard[old_pos[0], old_pos[1]]

        # check for capture
        if self.listLogicBoard[new_pos[0], new_pos[1]] is not None:
            self.unpersonPiece(self.listLogicBoard[new_pos[0], new_pos[1]])

        # update logic board
        self.listLogicBoard[old_pos[0], old_pos[1]] = None
        self.listLogicBoard[new_pos[0], new_pos[1]] = piece

        # update piece's first move
        if self.listLogicBoard[new_pos[0], new_pos[1]].firstMove:
            self.listLogicBoard[new_pos[0], new_pos[1]].firstMove = False

        # update piece's position
        piece.pos = new_pos

        # update graph board
        self.parent.updateGraphBoard(old_pos, new_pos)

        # check for upgrading time
        self.upgrading_time(new_pos)

        self.checkEndGame()

        # set up next turn
        if self.CPU_player:
            print("aaaaa")
        else:
            self.whiteTurn = not self.whiteTurn

        print(self.listLogicBoard[new_pos[0], new_pos[1]].getMoves(self.listLogicBoard))

    # check for win or tie
    def checkEndGame(self):
        # check for white win
        endgame = -999
        if str(self.black[4]) != "K0":
            endgame = 1
        # check for black win
        elif str(self.white[12]) != "K1":
            endgame = -1
        # check for insufficient material
        elif len(set(self.white+self.black)) == 3:
            endgame = 0

        if endgame != -999:
            self.isGameOver = True
            self.parent.endGame(endgame)

    # upgrade pawn to queen
    def upgrading_time(self, new):
        piece = self.listLogicBoard[new[0], new[1]]
        if piece.type == "P" and (new[0] == 0 or new[0] == 7):  # upgrading time
            self.listLogicBoard[new[0], new[1]] = Queen.Queen(piece.isWhite, new)
            self.parent.upgrading_time(new)

    # input: the captured piece
    # removes the piece from
    def unpersonPiece(self,casualty):
        if casualty.isWhite:
            self.white[casualty.serialNum] = None
        else:
            self.black[casualty.serialNum] = None

    # prints board
    def printBoard(self):
        for row in range(len(self.listLogicBoard)):
            print("")
            for col in range(len(self.listLogicBoard)):
                square = self.listLogicBoard[row, col]
                if square is None:
                    print("--", end=" ")
                else:
                    print(square, end=" ")
        print("")
