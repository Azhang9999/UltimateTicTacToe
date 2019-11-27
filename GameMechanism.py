
"""This File allows the user to run the game"""
import random
import copy
from deprecated import deprecated



count = 0
cache = {}

class BetterNormalGame(object):
    """ Better implementation of NormalGame """

    def __init__(self, )

@deprecated("this class is deprecated")
class NormalGame(object):

    def __init__(self, empty = [], cross = [], circle = [], xDict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}
                 , yDict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}, freeBoards = [], xBoards = [], oBoards = []):
        """ Initiates an empty board of ultimate tic tac toe
        Each coordinate is expressed by an integer from 0 to 9
        Each board is repressented by an integer from 0 to 9
        Each coordinates would be represented by a tuple
        (board number, square number)

        There is the following attributes:

        self.empty : a list of all of the empty squares
        self.cross : a list of all squares occupied by x team
        self.circle : a list of all square occupied by o team
        self.freeBoards : a list of all boards that can be maneuvered into
        self.xBoards: a list of all boards taken by x
        self.oBoards: a list of all boards taken by o
        self.winning: a list of all of the combinations that result in a win
        """
        self.empty = empty.copy()
        if len(self.empty) == 0:
            for x in range(1, 10):
                for y in range(1, 10):
                    self.empty.append((x,y))

        self.cross = cross.copy()
        self.circle = circle.copy()
        self.xDict = copy.deepcopy(xDict)
        self.yDict = copy.deepcopy(yDict)

        self.freeBoards = freeBoards.copy()
        if len(self.freeBoards) == 0:
            for x in range(1, 10):
                self.freeBoards.append(x)

        self.xBoards = xBoards.copy()
        self.oBoards = oBoards.copy()

        self.winning = [(1,2,3),(1,4,7),(1,5,9),(2,5,8),(3,5,7),(3,6,9),
                        (4,5,6),(7,8,9)]

    def copy(self):
        return NormalGame(self.empty.copy(), self.cross.copy(), self.circle.copy(), copy.deepcopy(self.xDict), copy.deepcopy(self.yDict), self.freeBoards.copy()
                          , self.xBoards.copy(), self.oBoards.copy())

    def get_circle(self):
        return self.circle.copy()

    def get_cross(self):
        return self.cross.copy()

    def show_row(self, row, board):
        """ returns the row of the board in the game"""
        cross = self.xDict[board]
        circle = self.yDict[board]
        line = ""
        for x in range(0,3):
            check = 3*row + x + 1
            line += "|"
            if check in cross:
                line += "X"
            elif check in circle:
                line += "O"
            else:
                line += " "
        return line + "|"

    def show_board(self, board):
        """ prints the position of everyone on the board"""

        answer = ""
        for x in range(0,3):
            answer += "-------\n"
            answer += show_row(x, board) +"\n"
        answer += "-------"
        return answer

    def show_game(self):
        """ Displays the whole layout of the game"""
        answer = ""
        for x in range(0,3):
            # x determins the big row number
            answer += "\n-------    -------    -------\n"
            for y in range(0,3):
                # y determins the rwo number
                for z in range(0,3):
                    # z determins the board number
                    answer += self.show_row((y), (x*3+z+1))+ "    "
                answer += "\n-------    -------    -------\n"
            answer += "\n"
        return answer


    def xMove(self, coordinate):
        """
        Assuming that the coordinate is in self.empty
        move it to self.cross
        returns the board of the next move
        """
        assert (coordinate in self.empty and coordinate not in self.cross)
        self.cross.append(coordinate)
        self.empty.remove(coordinate)
        self.xDict[coordinate[0]].append(coordinate[1])
        self.determineOwnership(1, coordinate[0])
        if coordinate[1] not in self.freeBoards:
            return None
        return coordinate[1]

    def oMove(self, coordinate):
        """
        Assuming that the coordinate is in self.empty
        move it to self.circle
        returns the board of the next move
        """
        assert (coordinate in self.empty and coordinate not in self.circle)
        self.circle.append(coordinate)
        self.empty.remove(coordinate)
        self.yDict[coordinate[0]].append(coordinate[1])
        self.determineOwnership(0, coordinate[0])
        if coordinate[1] not in self.freeBoards:
            return None
        return coordinate[1]

    def determineOwnership(self, side, board):
        """
        determine if anyone owns the board
        if ownership established
        move the board from freeBoards to owned boards of a particular side

        self - the game instance
        board - (int) the game instance
        side - 1 or 0 decides the side that is being checked
        """
        if side%2 == 1:
            if board in self.xBoards:
                return True
            played = self.xDict[board]
        else:
            if board in self.oBoards:
                return True
            played = self.yDict[board]
        if board not in self.freeBoards:
            return False
        for element in self.winning:
            answer = True
            for number in element:
                if number not in played:
                    answer = False
            if answer == True:
                self.freeBoards.remove(board)
                if side%2 == 1:
                    self.xBoards.append(board)
                else:
                    self.oBoards.append(board)
                return True
        full = True
        for element in self.empty:
            if element[0] == board:
                full = False
        if full:
            self.freeBoards.remove(board)
        return False

    def determineWinner(self):
        """ Returns the winner  ('x' or 'o') of the game or None if there is none"""
        for element in self.winning:
            cross = True
            circle = True
            for board in element:
                if board not in self.xBoards:
                    cross = False
                if board not in self.oBoards:
                    circle = False
            if cross == True:
                return 'x'
            elif circle == True:
                return 'o'
        return None

    def next_step(self, side, inp, board = None):
        """
        Plays the next step for the game
        returns the board choice of the next move or None if free reign
        (need to determine winner and ownership)

        side - 1('x') or 0('o') denoting the side that is playing
        inp - (<int>,<int>) denoting the coordinate that is being played
        board - the board that has to be placed on
        """
        assert self.determineWinner() == None, "{} already won".format(self.determineWinner())
        if board != None and board not in self.freeBoards:
            board = None
        if board != None:
            assert inp[0] == board
        if side%2 == 1:
            return self.xMove(inp)
        else:
            return self.oMove(inp)



class GameRunner(object):
    """ skeleton code for the program that runs the game,
        probably not going to be used directly"""
    def __init__(self):
        """ Creates an instance of gameRunner

            game - an instance of the NormalGame instance
            output - place whete it is outputed
            """
        self.game = NormalGame()




class RandomRunner(GameRunner):
    """ Computer plays against itself using random integers"""

    def run_game(self):
        coordinate = (random.randint(1, 9), random.randint(1, 9))
        side = 1
        board = None
        while self.game.determineWinner() == None and len(self.game.freeBoards) > 0:
            board = self.game.next_step(side%2, coordinate, board)
            if self.game.determineOwnership(side%2, coordinate[0]):
                board = None
            if board not in self.game.freeBoards:
                board = None
            side += 1
            if len(self.game.freeBoards) == 0:
                break
            if board == None:
                while coordinate not in self.game.empty or coordinate[0] not in self.game.freeBoards:
                    coordinate = (random.randint(1,9), random.randint(1, 9))
            else:
                while coordinate not in self.game.empty:
                    coordinate = (board, random.randint(1, 9))
        return (self.game.determineWinner(), self.game.cross, self.game.circle)


def statistical_runner():
    o = 0
    x = 0
    for y in range(0,100):
        print (y, o, x)
        runner = RandomRunner()
        if runner.run_game()[0] == 'x':
            x += 1
        else:
            o += 1
    print(o, x)

class TreeRunner(GameRunner):

    def next_turn(self, side, sideChecked, game, inp, board):
        def enter_cache(number):
            cross = game.get_cross().copy()
            cross.sort()
            cross = tuple(cross)
            circle = game.get_circle().copy()
            circle.sort()
            circle = tuple(circle)
            cache[(cross, circle, board, side)] = number
            File = open("UltimateTicTacToeData.out", 'a+')
            File.write(str(number)+ str(game.cross) + "," + str(game.circle) + "\n")
            File.close()
        def has_board():
            if board in game.freeBoards:
                listOfOkay = []
                overallScore = 0
                for element in game.empty:
                    if element[0] == board:
                        listOfOkay.append(element)
                for inp in listOfOkay:
                    score = self.next_turn((side+1)%2, sideChecked, game.copy(), inp, board)
                    if score == 1:
                        return 1
                    elif score == 0:
                        #print("has_board response")
                        return 0
                    else:
                        overallScore += score
                return overallScore / len(listOfOkay)
        board = game.next_step(side, inp, board)
##        if input() == 'n':
##            print(game.show_game())
        #print (game.determineWinner(), side, inp, game.xBoards, game.oBoards, game.circle)
        assert abs(len(game.cross)-len(game.circle)) <= 1
        #### CHECK CACHE ####
        cross = game.get_cross()
        cross.sort()
        cross = tuple(cross)
        circle = game.get_circle()
        circle.sort()
        circle = tuple(circle)
        if (cross, circle, board, side) in cache:
            return cache[(cross, circle, board, side)]
        #### CHECKING BASE CONDITIONS ####
        global count
        if game.determineWinner() == 'x':
            enter_cache(1)
            count = count + 1
            print(count)
            #print("WE WON")
            return 1
        elif game.determineWinner() == 'o':
            enter_cache(0)
            #print ("ENTERED: ", game.circle)
            #print ("---------------------------------")
            count += 1
            print(count)
            return 0
        elif len(game.freeBoards) == 0:
            assert game.determineWinner() == None, "actual winner : {}".format(game.determineWinner())
            enter_cache(0.5)
            #print ("---------------------------------")
            count += 1
            print(count)
            return 0.5
        #### RUNNING NEXT LEVEL ####
        else:
            if board in game.freeBoards:
                x = has_board()
                enter_cache(x)
                if x == 0:
                    return 0.01
                elif x == 1:
                    return 0.99
                return x
            else:
                answer = 0
                for board in game.freeBoards:
                    x = has_board()
                    if x == 0:
                        enter_cache(0.01)
                        return 0.01
                    elif x == 1:
                        enter_cache(0.99)
                        return 0.99
                    answer += x
                answer = answer / len(game.freeBoards)
                enter_cache(answer)
                return answer



    def run_game_first(self):
        """runs the code and do a depth first search for the best solution
            Going to be fun

            IMPLEMENTED RECURSIVELY
            1) Base case: determineOwnership evaluates to True or no more free boards
            The level before determineOwnership evaluates to true has 100% win rate
            2) recursion: step by step
            3) each branch has same weight in win probability
            4) goal: create something with max win probability

            USE next_turn to do recursion
            """
        File = open('UltimateTicTacToeData.out', 'w')
        File.write('START')
        File.close()
        firstMoveDict = {}
        for x in range(1,10):
            for y in range(1, 10):
                print("Branch in progress:", (x,y))
                firstMoveDict[(x,y)] = self.next_turn(1, 'x', self.game.copy(), (x, y), None)
        return firstMoveDict

#statistical_runner()

##game = NormalGame()
##game.xMove((1,1))
##game.xMove((1,2))
##game.xMove((1,3))
##print(game.show_game())
##print(game.determineOwnership(2, 'x'))
