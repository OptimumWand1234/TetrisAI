from board import Direction, Rotation, Board
from random import Random
import time

class Player:

    def findHighest(self, scores):

        max = - 9999999999999
        index = 0
        for score in scores:
            if score > max:
                max = score
                maxInd = index
            index += 1
        return maxInd

    def choose_action(self, board):

        return self.choose_best_action(board)

    def choose_best_action(self, board):

        print(self.holes(board))

        scores = []
        rotSh = []
        listMoves = []
        scores2 = []

        for rotations in range(0, 4):
            for xcoor in range(0, 10):
                test_board = board.clone()
                scores.append(self.moveBoard(test_board, rotations, xcoor))
                rotSh.append((rotations, xcoor))
                scores2 = []
                for rotations2 in range(0, 4):
                    for xcoor2 in range(0, 10):
                        test_board2 = test_board.clone()
                        scores2.append(self.moveBoard(test_board2, rotations2, xcoor2))

                scores[-1] += max(scores2)

        board2 = board.clone()
        index = self.findHighest(scores)

        rot = rotSh[index][0]
        xpos = rotSh[index][1]

        while rot > 0:
            listMoves.append(Rotation.Clockwise)
            board2.rotate(Rotation.Clockwise)
            rot -= 1

        if (xpos < board2.falling.left):
            nshifts = board2.falling.left - xpos

            while nshifts > 0 and board2.falling:
                listMoves.append(Direction.Left)
                board2.move(Direction.Left)
                nshifts -= 1

        elif (xpos > board2.falling.left):
            nshifts = xpos - board2.falling.left
            while nshifts > 0 and board2.falling and board2.falling.right < 9:
                listMoves.append(Direction.Right)
                board2.move(Direction.Left)
                nshifts -= 1

        listMoves.append(Direction.Drop)
        board.place_next_block()

        return listMoves

    def moveBoard(self, board, rotations, xcoor):

        completeLines = self.maxHeight(board)

        if (board.falling):
            self.rotateBlock(board, rotations)

        if (board.falling):
            self.shiftBlock(board, xcoor)

        if (board.falling):
            board.move(Direction.Drop)

        completeLines -= self.maxHeight(board)

        return self.scoreTheMove(board, completeLines)

    def shiftBlock(self, board, xcoor):

        if (xcoor < board.falling.left):

            nshifts = board.falling.left - xcoor

            while nshifts > 0 and board.falling:
                board.move(Direction.Left)
                nshifts -= 1

        elif (xcoor > board.falling.left):
            nshifts = xcoor - board.falling.left
            while nshifts > 0 and board.falling and board.falling.right < 9:
                board.move(Direction.Right)
                nshifts -= 1
        else:
            if (board.falling):
                board.move(Direction.Down)

    def rotateBlock(self, board, rotations):

        while rotations > 0 and board.falling:
            board.rotate(Rotation.Clockwise)
            rotations -= 1

    def countCells(self, board):
        counter = 0

        for x in range(board.width):
            for y in range(board.height):
                if (x, y) in board.cells:
                    counter += 1

        return counter

    def aggHeight(self, board):

        aggHeight = 0
        for x in range(board.width):
            count = 0
            for y in range(board.height):
                if (x, y) in board.cells:
                    count = board.height - y
                    break
            aggHeight += count

        return aggHeight

    def maxHeight(self, board):

        maxs = []
        max_height = 0
        for x in range(board.width):
            for y in range(board.height):
                if (x, y) in board.cells:
                    maxs.append(board.height - y)
                    break

        if maxs:
            max_height = max(maxs)

        return max_height

    def height_diff(self, board):
        hs = []
        max_height = 0
        min_height = 0

        seen = False

        for x in range(board.width):
            seen = False
            for y in range(board.height):
                if (x, y) in board.cells:
                    hs.append(board.height - y)
                    seen = True
                    break
            if not seen:
                hs.append(0)
        if hs:
            max_height = max(hs)
            min_height = min(hs)

        return max_height - min_height

    def holes(self, board):
        holes = 0
        counter = 1
        for x in range(board.width):
            for y in range(1, board.height):

                if (x, y) not in board.cells and (x, y - 1) in board.cells:
                    holes += 1
                    counter = 1
                    while((x, y+counter) not in board.cells and y+counter < board.height-1):
                        holes += 1
                        counter += 1
        return holes

    def bumpiness(self, board):
        bumpiness = 0
        for x in range(board.width - 1):
            count = 0
            count2 = 0
            found1 = False
            found2 = False
            for y in range(board.height):
                if (x, y) in board.cells and not found1:
                    count = board.height - y
                    found1 = True
                if (x + 1, y) in board.cells and not found2:
                    count2 = board.height - y
                    found2 = True
                if found1 and found2:
                    break
            bumpiness += abs(count - count2)
        return bumpiness

    def scoreTheMove(self, board, completeLines):
        c1 = -2  # Agg height
        c2 = 100  # completeLines
        c3 = -22  # holes
        c4 = -0.9  # bumpiness
        c5 = -10  # height difference

        aggHeight = self.aggHeight(board)
        holes = self.holes(board)
        bumpiness = self.bumpiness(board)
        heighDifference = self.height_diff(board)
        maxH = self.maxHeight(board)

        if maxH>7:
            c2 *= 5
            c5 *= 2
            c3 *= 2
        score = ((c1 * aggHeight) + (c2 * completeLines) + (c3 * holes) + (c4 * bumpiness) + (c5*heighDifference))

        return score

SelectedPlayer = Player
