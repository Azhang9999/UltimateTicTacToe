
"""This File allows the user to run the game"""
import random
import copy
#from deprecated import deprecated



count = 0
cache = {}

class BetterNormalGame(object):
    """
    Better implementation of NormalGame
    cross = 1 and circle = -1 universally in this version
    blank space = 0
    board represented by a 2D list
    if a side ever wins a board, the whole tuple is replaced with the
    int value of the side that won it
    """
    winning = [(0, 1, 2), (0, 3, 6), (0, 4, 8), (1, 4, 7), (2, 4, 6), (2, 5, 8), (3, 4, 5), (6, 7, 8)]
    cross = 1
    circle = -1
    none_coordinate = (10, 10)

    def __init__(self, game = None):
        ## Copying the existing game
        if game != None:
            self.universe = game.get_universe()
            self.must_move_board = game.get_must_move_board()
            return
        ## Creating a new game bc no game is passed in
        else:
            self.universe = []
            for i in range(9):
                self.universe.append([])
                for _ in range(9):
                    self.universe[i].append(0)
        self.must_move_board = None

    def get_universe(self):
        return self.universe.copy()

    def get_must_move_board(self):
        return self.must_move_board

    def convert_side_int_to_str(side_int):
        if side_int == BetterNormalGame.cross:
            return "X"
        elif side_int == BetterNormalGame.circle:
            return "O"
        return " "

    def show_row(self, row, board):
        """ returns the row of the board in the game"""
        if isinstance(self.universe[board], int):
            side = BetterNormalGame.convert_side_int_to_str(self.univers[board])
            return "|" + side + "|" + side + "|" + side + "|"
        line = ""
        for x in range(0, 3):
            check = 3 * row + x
            line += "|" + BetterNormalGame.convert_side_int_to_str(self.universe[board][check])
        return line + "|"

    def show_board(self, board):
        """ prints the position of everyone on the board"""
        answer = ""
        for x in range(0, 3):
            answer += "-------\n"
            answer += self.show_row(x, board) +"\n"
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
                    answer += self.show_row((y), (x*3+z))+ "    "
                answer += "\n-------    -------    -------\n"
            answer += "\n"
        return answer

    def determineOwnership(self, board_number):
        """
        determine if anyone owns the board
        returns the owner or None otherwise
        board marked as owned if anyone owns the boards

        self - the game instance
        board_number - (int) the game instance
        """
        board = self.universe[board_number]
        if isinstance(board, int):
            return board
        for item in self.winning:
            score = 0
            for spot in item:
                score += board[spot]
            if score == 3 * self.cross:
                self.universe[board_number] = self.cross
                return self.cross
            elif score == 3 * self.circle:
                self.universe[board_number] = self.circle
                return self.circle
        return None

    def determineWinner(self):
        """ Returns the winner (self.circle or self.cross) of the game or None """
        taken_board = {}
        for item in self.winning:
            score = 0
            for board in item:
                if isinstance(self.universe[board], int):
                    taken_board[board] = int
                    score += board
            if score == 3 * self.cross:
                return self.cross
            elif score == 3 * self.circle:
                return self.circle
        if len(taken_board) == 9:
            return 0
        return None

    def move(self, side, coordinate):
        """
        Assuming that the coordinate is unoccupied
        let the side make the move
        and check ownership and change must_move_board
        """
        assert (self.universe[coordinate[0]][coordinate[1]] == 0)
        self.universe[coordinate[0]][coordinate[1]] = side
        self.determineOwnership(coordinate[0])
        self.must_move_board = coordinate[1]
        if isinstance(self.universe[coordinate[1]], int):
            self.must_move_board = None

    def next_step(self, side, inp):
        """
        Plays the next step for the game
        returns the board choice of the next move or None if free reign
        (need to determine winner and ownership)

        side - self.circle or self.cross denoting the side that is playing
        inp - (<int>,<int>) denoting the coordinate that is being played
        board - the board that has to be placed on
        """
        assert self.determineWinner() == None, "{} already won".format(BetterNormalGame.convert_side_int_to_str(self.determineWinner()))
        if self.must_move_board != None and isinstance(self.universe[inp[0]], int):
            self.must_move_board = None
        if self.must_move_board != None:
            assert inp[0] == self.must_move_board
        self.move(side, inp)


    def is_coord_valid(self, coordinate):
        if coordinate == self.none_coordinate:
            return False
        if isinstance(self.universe[coordinate[0]], int):
            return False
        if self.universe[coordinate[0]][coordinate[1]] != 0:
            return False
        if self.must_move_board != None and coordinate[0] != self.must_move_board:
            return False
        return True

class GameRunner(object):
    """ skeleton code for the program that runs the game,
        probably not going to be used directly"""
    def __init__(self):
        """ Creates an instance of gameRunner

            game - an instance of the NormalGame instance
            output - place whete it is outputed
            """
        self.game = BetterNormalGame()


class RandomRunner(GameRunner):
    """ Computer plays against itself using random integers"""

    def run_game(self):
        coordinate = (random.randint(0, 8), random.randint(0, 8))
        side = 1
        while self.game.determineWinner() == None:
            board = self.game.get_must_move_board()
            coordinate = self.game.none_coordinate
            while coordinate == None or not self.game.is_coord_valid(coordinate):
                coordinate = (board, random.randint(0, 8))
                if board != None:
                    coordinate = (random.randint(0, 8), coordinate[1])
            self.game.next_step(side, coordinate)
            side = -1 * side
        return (self.game.determineWinner())


def statistical_runner():
    o = 0
    x = 0
    for y in range(0,100):
        print (y, o, x)
        runner = RandomRunner()
        if runner.run_game()[0] == BetterNormalGame.cross:
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

if __name__ == "__main__":
    statistical_runner()
