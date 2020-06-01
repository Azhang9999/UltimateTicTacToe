from GameMechanism import *
import ast

def read_data():
    File = open("UltimateTicTacToeData.out",'r')
    firstGame = File.readline()
    space = firstGame.find('[')
    score = float(firstGame[5:space])
    print("SCORE: ", score)
    evaluate = firstGame[space:]
    first = ast.literal_eval(evaluate)
    print (first)
    File.close()
    return first

def line_read(File):
    while input() == 'Next':
        firstGame = File.readline()
        space = firstGame.find('[')
        try:
            score = float(firstGame[:space])
        except:
            score = float(firstGame[5:space])
        print("SCORE: ", score)
        evaluate = firstGame[space:]
        first = ast.literal_eval(evaluate)
        print (first)
        game = step_game(first)
        print(game.show_game())

def create_final_game(first):
    game = NormalGame([],first[0],first[1])
    return game

def step_game(first):
    game = NormalGame()
    for x in range(0,min(len(first[0]),len(first[1]))):
        assert game.determine_winner() == None, str(x) + str(first[0][x]) + str(first[1][x]) + str(
            game.determine_winner()) + str(game.cross) + str(game.circle)
        game.xMove(first[0][x])
        game.oMove(first[1][x])
    if len(first[0]) < len(first[1]):
        game.oMove(first[1][len(first[1])])
    elif len(first[0]) > len(first[1]):
        game.xMove(first[0][len(first[0])])
    return game


def read():
    File = open("UltimateTicTacToeData.out",'r')
    line_read(File)
    File.close()

read()

##game = NormalGame()
##game.xMove((1,1))
##left = NormalGame()
##left.get_cross()
##
##class Normal(object):
##    
##    def __init__ (self, list1 = []):
##        self.list1 = list1
##        
##    def append(self, number):
##        self.list1.append(number)
##    
##game = Normal()
##game.append(4)
##left = Normal()
##print (left.list1)
