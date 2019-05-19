from GameMechanism import *

def newGame():  
    run = 'y'
    while run == 'y':
        gameRunner()
        run = input('start new game?')
    

def gameRunner():
    game = NormalGame()
    side = 1
    board = None
    while(game.determineWinner()==None):
        print(game.show_game())
        inp = (0,0)
        if board == None:
            print ('you can move in any board')
            inp = input('please move')
            inp = eval(inp)
        else:
            while inp[0] != board:
                print ('you can move in the board', board)
                inp = input('please move')
                inp = eval(inp)
        board = game.next_step(side, inp, None)
        side += 1

if __name__ == "__main__":
    newGame()


