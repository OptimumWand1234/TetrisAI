from board import Direction, Rotation, Board
from random import Random
import time



class Player:



    def findHighest(self, scores):

        max = - 9999
        index = 0

        for score in scores:
            index += 1
            if score > max:
                max = score

        return index-1



    def choose_action(self, board):

        self.choose_best_action(board)


    def choose_best_action(self, board):
        scores = []
        rotSh = []
        listMoves = []

        for rotations in range (0, 4):
            for shifts in range (0, 10):
                test_board = board.clone()
                self.moveBoard(test_board, rotations, shifts)
                scores.append(self.scoreTheMove(test_board))
                rotSh.append((rotations, shifts))

        index = self.findHighest(scores)

        rot = rotSh[index][0]
        sh = rotSh[index][1]

        self.moveBoard(board, rot, sh)




    def moveBoard(self, board, rotations, shifts):

        self.shiftBlock(board, shifts)
        self.rotateBlock(board, rotations)
        board.falling.move(Direction.Drop, board)

    def shiftBlock(self, board, shifts):
        if (shifts < 5):
            nshifts = board.falling.left - shifts
            while (nshifts > 0):
                board.falling.move(Direction.Left, board)
                nshifts -= 1
        else:
            nshifts = shifts - board.falling.right
            while nshifts > 0:
                board.falling.move(Direction.Right, board)
                nshifts -= 1


    def rotateBlock(self, board, rotations):

        while rotations > 0:
            board.falling.rotate(Rotation.Clockwise, board)
            rotations -= 1

    def scoreTheMove(self, board):

        aggHeight = 0
        completeLines = 0
        holes = 0

        for x in range(board.width):
            count = 0
            for y in range(board.height):
                if (x, y) in board.cells:
                    count = y
            aggHeight += count

        for y in range(board.height):
            counter = 0
            for x in range(board.width):
                if (x, y) in board.cells:
                    counter += 1
            if counter == board.width:
                completeLines += 1

        for y in range(1, board.height):
            for x in range(board.width):
                if (x, y) not in board.cells and (x, y - 1) in board.cells:
                    holes += 1

        return ((-0.51 * aggHeight) + (0.76 * completeLines) + (-0.36 * holes))


# class RandomPlayer(Player):
#     def __init__(self, seed=None):
#         self.random = Random(seed)
#         self.direction = [None]
#
#
#     def add_dir(self):
#         if self.direction != None:
#             if self.direction[-1] == Direction.Right:
#                 self.direction.append(Direction.Left)
#                 self.direction.append(Direction.Left)
#                 return
#
#             self.direction.append(Direction.Right)
#             self.direction.append(Direction.Right)
#             return
#
#     def choose_action(self, board):
#         if board.move(Direction.Right) or board.rotate(Rotation.Clockwise):
#             time.sleep(2)
#         yield Direction.Right
#         yield Rotation.Clockwise
#



SelectedPlayer = Player
/*

def scoreTheMove(self, board):
    aggHeight = 0
    completeLines = 0
    holes = 0

    for x in range(board.width):
        count = 0
        for y in range(board.height):
            if (x, y) in board.cells:
                count = y
        aggHeight += count

    for y in range(board.height):
        counter = 0
        for x in range(board.width):
            if (x, y) in board.cells:
                counter += 1
        if counter == board.width:
            completeLines += 1

    for y in range(1, board.height):
        for x in range(board.width):
            if (x, y) not in board.cells and (x, y - 1) in board.cells:
                holes += 1
    print(f"{aggHeight} {completeLines} {holes}")
    score = ((-0.51 * aggHeight) + (0.76 * completeLines) + (-0.36 * holes))

    return score

*/