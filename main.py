import numpy as np
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.layout import Layout

from controller import Controller


class Cell(Button):  # MAKE A BUTTON
    def __init__(self, row, col):
        Button.__init__(self)
        self.bold = False
        self.font_size = 40
        self.row = row  # cell's row
        self.col = col  # cell's col


class Board(GridLayout):  # Making a randomized chess board

    def __init__(self, difficulty, menu):
        GridLayout.__init__(self)
        self.cols = 8
        self.listGraphBoard = self.buildGraphBoard()
        self.controller = Controller(self.cols, self)
        self.addCellsToBoard()
        self.movingPiece = None
        self.difficulty = difficulty
        self.menu = menu

    # output: an empty graphic board
    def buildGraphBoard(self):
        return np.empty((self.cols, self.cols), dtype=Cell)

    # reacting to user's press
    def reaction(self, b1):
        if self.controller.isGameOver:
            self.menu.rebuild_menu()
        else:
            if self.movingPiece is None:
                if self.controller.listLogicBoard[b1.row, b1.col] is not None:
                    # checks if the player is clicking on a piece
                    self.movingPiece = (b1.row, b1.col)
                    b1.background_color = [0, 0, 1, 1]
            else:
                self.listGraphBoard[self.movingPiece[0], self.movingPiece[1]].background_color = [1, 1, 1, 1]
                if self.controller.isLegal(self.movingPiece, (b1.row, b1.col)) and not self.movingPiece == (
                b1.row, b1.col):
                    self.controller.logMove(self.movingPiece, (b1.row, b1.col))
                    self.controller.printBoard()

                self.movingPiece = None

    # adds cells to graphic board
    def addCellsToBoard(self):
        for row in range(self.cols):
            for col in range(self.cols):
                temp_cell = Cell(row, col)
                temp_cell.background_color = [0, 0, 0, 0]
                if self.controller.listLogicBoard[row, col] is not None:
                    temp_cell.background_color = [1, 1, 1, 1]
                    temp_cell.background_down = temp_cell.background_normal = "img/" + str(
                        self.controller.listLogicBoard[
                            row, col]) + ".png"
                temp_cell.bind(on_press=self.reaction)
                self.listGraphBoard[row, col] = temp_cell
                self.add_widget(temp_cell)

    # recolor pieces accourding to game type: lose, tie, win (for the computer)
    def recolour(self, type):
        for row in self.listGraphBoard:
            for square in row:
                if square.background_color != [0, 0, 0, 0]:
                    if type == -1:
                        square.background_color = [0, 1, 0, 1]
                    elif type == 0:
                        square.background_color = [0, 1, 1, 1]
                    elif type == 1:
                        square.background_color = [1, 0, 0, 1]

    # updates graph board
    def updateGraphBoard(self, old_pos, new_pos):
        self.listGraphBoard[old_pos[0], old_pos[1]].background_color = [0, 0, 0, 0]
        self.listGraphBoard[new_pos[0], new_pos[1]].background_color = [1, 1, 1, 1]
        self.listGraphBoard[new_pos[0], new_pos[1]].background_down = self.listGraphBoard[
            new_pos[0], new_pos[1]].background_normal = "img/" + str(
            self.controller.listLogicBoard[new_pos[0], new_pos[1]]) + ".png"

    # change pawn to queen on graphic board
    def upgrading_time(self, new):
        self.listGraphBoard[new[0], new[1]].background_down = self.listGraphBoard[
            new[0], new[1]].background_normal = "img/" + str(
            self.controller.listLogicBoard[new[0], new[1]]) + ".png"


class Game(Layout):
    def __init__(self, difficulty, parent):
        Layout.__init__(self)

        self.background = Image(source="img/background.png")
        self.background.pos = (0, 0)
        self.background.size = (820, 820)

        self.board = Board(difficulty, parent)
        self.board.pos = (0, 0)
        self.board.size = (820, 820)

        self.add_widget(self.background)
        self.add_widget(self.board)


Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '820')
Config.set('graphics', 'height', '820')
Config.write()
