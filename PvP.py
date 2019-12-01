from GameMechanism import *

def new_game():
    run = 'y'
    while run == 'y':
        game_runner()
        run = input('start new game?')


def game_runner():
    game = BetterNormalGame()
    side = 1
    while game.determineWinner()==None:
        print(game.show_game())
        inp = (0,0)
        if game.get_must_move_board() == None:
            print ('you can move in any board')
            inp = input('please move')
            inp = eval(inp)
        else:
            while inp[0] != board:
                print ('you can move in the board', game.get_must_move_board())
                inp = input('please move')
                inp = eval(inp)
        side += 1

if __name__ == "__main__":
    new_game()
