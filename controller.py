import copy

import numpy as np
from kivy.clock import Clock

from Model import Talos
from pieces import King, Rook, Knight, Bishop, Queen, Pawn


class Controller:  # keeps the logic board and rules of the game
    def __init__(self, cols, parent):

        self.black = []  # black pieces
        self.white = []  # white pieces

        self.listLogicBoard = self.buildLogicBoard(cols)
        self.whiteTurn = True
        self.parent = parent
        self.isGameOver = False

        self.route = []

    # input: the number of lines\cols
    # output: a logic board with every position set to 'empty'
    def buildLogicBoard(self, cols):
        board = np.full((cols, cols), None)

        # [R - rook , N - knight , B - bishop , Q - queen , P - pawn]
        pieces = ["R", "N", "B", "Q", "K", "B", "N", "R", "P", "P", "P", "P", "P", "P", "P", "P"]
        serial = 0
        # add pieces to top lines
        options = copy.deepcopy(pieces)
        for row in range(2):
            for col in range(len(board)):
                piece = self.createPiece(options[0], False)  # add black piece
                piece.pos = (row, col)
                piece.serialNum = serial

                serial += 1
                self.black.append(piece)
                board[row, col] = piece

                options.pop(0)

        serial = 0
        # add pieces to bottom lines
        options = copy.deepcopy(pieces)
        for row in range(6, 8):
            for col in range(len(board)):
                piece = self.createPiece(options[-1], True)  # add white piece

                # fix queen and king positions
                if row == 7:
                    if col == 3:
                        piece = self.createPiece("Q", True)
                    elif col == 4:
                        piece = self.createPiece("K", True)

                piece.pos = (row, col)
                piece.serialNum = serial

                serial += 1
                self.white.append(piece)
                board[row, col] = piece

                options.pop(-1)

        return board

    # creates an instance of a piece by type and side (black\white)
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
        if type == "K":
            return King.King(isWhite, (-999, -999), -999)

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
            captured = self.listLogicBoard[new_pos[0], new_pos[1]]
            self.DeletePiece(captured)

        # update logic board
        self.listLogicBoard[old_pos[0], old_pos[1]] = None
        self.listLogicBoard[new_pos[0], new_pos[1]] = piece

        # update piece's first move
        if self.listLogicBoard[new_pos[0], new_pos[1]].firstMove:
            self.listLogicBoard[new_pos[0], new_pos[1]].firstMove = False

            # check for castling
            if piece.type == "K":
                if new_pos[1] == 2:
                    self.castle([new_pos[0],0],[new_pos[0],3])
                elif new_pos[1] == 6:
                    self.castle([new_pos[0],7],[new_pos[0],5])

        # update piece's position
        piece.pos = new_pos

        # check for upgrading time
        self.upgrading_time(new_pos)

        # update graph board
        self.parent.updateGraphBoard(old_pos, new_pos)

        endgame = self.checkEndGame()
        if endgame == -999:
            # set up next turn
            self.whiteTurn = not self.whiteTurn

            if not self.whiteTurn:
                Clock.schedule_once(self.computer_turn, 0.1)

        else:
            self.isGameOver = True
            self.parent.recolour(endgame)

    # checks if last board is occurred more than 3 times
    def hasRepeated(self, route):
        if len(route) == 0:
            return False
        board = route[-1][0]
        times = 0
        for index in range(len(route) - 1):
            if board == route[index][0]:
                times += 1
                if times > 3:
                    return True
        return False

    # check for endgame
    def checkEndGame(self):
        # check for white win
        endgame = -999
        if str(self.black[4]) != "K0":
            print("--white wins--")
            endgame = -1
        # check for black win
        elif str(self.white[12]) != "K1":
            print("--black wins--")
            endgame = 1
        # check for insufficient material
        elif len(set(self.white + self.black)) == 4:
            print("--insufficient material--")
            endgame = 0
        # check for repeated action
        elif self.hasRepeated(self.route):
            print("--repeated action--")
            endgame = 0

        return endgame

    # update computer's turn
    def computer_turn(self, t1):
        next_move = Talos.make_move(self.listLogicBoard, self.black, self.white, self.parent.difficulty)
        self.logMove(next_move[0], next_move[1])

    # upgrade pawn to queen
    def upgrading_time(self, new):
        piece = self.listLogicBoard[new[0], new[1]]
        if piece.type == "P" and (new[0] == 0 or new[0] == 7):  # upgrading time
            self.listLogicBoard[new[0], new[1]] = Queen.Queen(piece.isWhite, new, piece.serialNum)
            self.parent.upgrading_time(new)

    # moves rook to castle
    def castle(self,old_pos, new_pos):
        piece = self.listLogicBoard[old_pos[0], old_pos[1]]

        # update logic board
        self.listLogicBoard[old_pos[0], old_pos[1]] = None
        self.listLogicBoard[new_pos[0], new_pos[1]] = piece

        # update piece's first move
        self.listLogicBoard[new_pos[0], new_pos[1]].firstMove = False

        # update piece's position
        piece.pos = new_pos

        # update graph board
        self.parent.updateGraphBoard(old_pos, new_pos)


    # input: the captured piece
    # removes the piece from pieces array
    def DeletePiece(self, casualty):
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
