class Piece:
    def __init__(self,isWhite,pos,type,serial):
        self.isWhite = isWhite
        self.pos = pos  # piece's pos
        self.type = type  # piece type (rook,pawn,queen, ect.)
        self.value = -999  # piece's value
        self.serialNum = serial
        self.firstMove = True # has the piece moved

    def __str__(self):
        return self.type + str(int(self.isWhite))
