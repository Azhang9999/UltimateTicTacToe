
"""This File allows the user to run the game"""
import random
import copy
from statistics import mean
from deprecated import deprecated
import json

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

    def __init__(self, game=None):
        # Copying the existing game
        if game:
            self.universe = game.get_universe()
            self.must_move_board = game.get_must_move_board()
        # Creating a new game bc no game is passed in
        else:
            self.universe = []
            for i in range(9):
                self.universe.append([])
                for _ in range(9):
                    self.universe[i].append(0)
            self.must_move_board = None

    def get_universe(self):
        return copy.deepcopy(self.universe)

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
            side = BetterNormalGame.convert_side_int_to_str(self.universe[board])
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
        for x in range(0, 3):
            # x determines the big row number
            answer += "\n-------    -------    -------\n"
            for y in range(0, 3):
                # y determines the row number
                for z in range(0, 3):
                    # z determines the board number
                    answer += self.show_row((y), (x*3+z)) + "    "
                answer += "\n-------    -------    -------\n"
            answer += "\n"
        return answer

    def __str__(self):
        return self.show_game()

    def determine_ownership(self, board_number):
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
        if 0 not in board:
            self.universe[board_number] = 0
            return 0
        return None

    def determine_winner(self):
        """ Returns the winner (self.circle or self.cross) of the game or None """
        taken_board = {}
        for item in self.winning:
            score = 0
            for board in item:
                if isinstance(self.universe[board], int):
                    taken_board[board] = int
                    score += self.universe[board]
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
        self.determine_ownership(coordinate[0])
        self.determine_ownership(coordinate[1])
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
        """
        assert not self.determine_winner(), "{} already won".format(BetterNormalGame.convert_side_int_to_str(
            self.determine_winner()))
        self.move(side, inp)

    def is_coord_valid(self, coordinate):
        """
        Checks if the coordinate is a valid coordinate. Non valid coordinate includes the None coordinate,
        coordinate that is already taken, coordinate that is in a board that is already taken, and coordinate that
        is not in a board that the coordinate is being restricted to.
        """
        if coordinate == self.none_coordinate:
            return False
        if isinstance(self.universe[coordinate[0]], int):
            return False
        if self.universe[coordinate[0]][coordinate[1]] != 0:
            return False
        if self.must_move_board and coordinate[0] != self.must_move_board:
            return False
        return True

    def all_valid_coord(self):
        """returns all valid coordinates
        """
        if self.must_move_board:
            first = self.must_move_board
            sols = [(first, i) for i in range(len(self.universe[first])) if self.universe[first][i] == 0]
            return sols
        else:
            sols = []
            for first in range(len(self.universe)):
                if not isinstance(self.universe[first], int):
                    for second in range(len(self.universe[first])):
                        if not self.universe[first][second]:
                            sols.append((first, second))
            return sols

    def __eq__(self, other):
        if not other:
            return False
        if self.universe != other.get_universe():
            return False
        if self.must_move_board != other.get_must_move_board():
            return False
        return True
    
    def __hash__(self):
        return self.__str__().__hash__()

    def __repr__(self):
        return str(self.universe) + str(self.must_move_board)


class GameRunner(object):
    """ skeleton code for the program that runs the game,
        probably not going to be used directly"""
    def __init__(self, game=None):
        """ Creates an instance of gameRunner

            game - an instance of the NormalGame instance
            """
        if game:
            self.game = BetterNormalGame(game)
        else:
            self.game = BetterNormalGame()

class RandomRunner(GameRunner):
    """ Computer plays against itself using random integers"""

    def run_with_all_valid_coords(self):
        side = 1
        while self.game.determine_winner() == None:
            all_coords = self.game.all_valid_coord()
            curr_coords = random.choice(all_coords)
            assert self.game.is_coord_valid(curr_coords)
            self.game.next_step(side, curr_coords)
            side = -1 * side
        return self.game.determine_winner()

    @deprecated
    def run_game(self):
        """
        Runs a game randomly until it finishes.
        :returns: an int representing the winner of the game that is run randomly
        """
        side = 1
        while not self.game.determine_winner() and self.game.determine_winner() != 0:
            self.game.show_game()
            board = self.game.get_must_move_board()
            coordinate = self.game.none_coordinate
            while not self.game.is_coord_valid(coordinate):
                coordinate = (board, random.randint(0, 8))
                if not board:
                    coordinate = (random.randint(0, 8), coordinate[1])
            self.game.next_step(side, coordinate)
            side = -1 * side
        return self.game.determine_winner()


def statistical_run(times):
    """
    Makes a Random Runner class and runs the game randomly times amount

    :arg times: the amount of times that random game is run
    :return: the results of running the game randomly times amount
    """
    o = 0
    x = 0
    for y in range(0, times):
        runner = RandomRunner()
        result = runner.run_with_all_valid_coords()
        if result == BetterNormalGame.cross:
            x += 1
        elif result == BetterNormalGame.circle:
            o += 1
    print(o, x)


class TreeRunner(GameRunner):
    cache = {}

    def dfs(self, side):
        curr_winner = self.game.determine_winner()
        if curr_winner != None:
            self.cache_results(side, curr_winner)
            return self.game.determine_winner()
        if (self.game, side) in self.cache:
            return self.cache[(self.game, side)]
        rest_results = []
        for i in self.game.all_valid_coord():
            branch = TreeRunner(self.game)
            branch.game.next_step(side, i)
            rest_results.append(branch.dfs(side*-1))
        results = mean(rest_results)
        self.cache_results(side, results)
        return results

    def cache_results(self, side, results):
        TreeRunner.cache[(self.game, side)] = results
        self.write_as_json()

    def write_as_json(self):
        with open("dfs_tree_results.json", "w") as f:
            k = self.cache.keys()
            v = self.cache.values()
            k1 = [str(i) for i in k]
            json.dump(json.dumps(dict(zip(*[k1, v])), indent=4), f)

    def write_as_text(self, side, results):
        file = open("UltimateTicTacToeData.out", 'a+')
        file.write(str(self.game) + str(side) + "\n" + str(results) + "\n")
        file.close()

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
        file = open('UltimateTicTacToeData.out', 'w')
        file.write("START")
        file.close()
        return self.dfs(BetterNormalGame.cross)


if __name__ == "__main__":
    runner = TreeRunner()
    runner.run_game_first()
