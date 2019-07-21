from GameMechanism import *

class bfsrunner(GameRunner):
    def __init__(self, game):
        self.gameBoard = NormalGame()
        self.que = []
        self.nextQue = []
        self.STEPSCONSIDERED = 5
        self.BOARDWORTH = {1:3, 2:2, 3:3, 4:2, 5:4, 6:2, 7:3, 8:2, 9:3}

    def processBoard(self, side, board):
        """
        calculates the best moves for the side that is specified.
        INPUT: side: 1 ('x') or 0 ('o')
        OUTPUT: all of the results in a self.que
        """
        self.que.append(self.gameBoard.copy())
        for i in range(0, self.STEPSCONSIDERED):
            for item in self.que:
                self.enque(side, item[0], item[1])
            self.que = self.nextQue
            self.nextQue = []
            for item in self.que:
                self.enque((side+1)%2, item[0], item[1])
            self.que = self.nextQue
            self.nextQue = []

    def enque(self, side, game, board):
        """
        helper method that puts all of the possible options in the que
        :param side: the side that is being played on (1 for x and 0 for o)
        :param game: the current step of the game
        :param board: the board that is being considered
        :return: nothing
        """
        if board == None:
            for i in range(1, 10):
                self.enque(side, game, i)
        else:
            for i in range(1, 10):
                newGame = game.copy()
                newBoard = newGame.next_step(side, (board, i))
                self.nextQue.append((newGame, newBoard))

    def findWorth(self, listOfBoards):

