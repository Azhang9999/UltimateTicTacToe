from GameMechanism import *

def new_game():
    run = 'y'
    while run == 'y':
        game_runner()
        run = input('start new game?')


def game_runner():
    game = BetterNormalGame()
    side = game.cross
    while game.determineWinner() == None:
        print (game.show_game())
        if game.get_must_move_board() == None:
            print ('you can move in any board')
            inp = input('please move')
            inp = eval(inp)
        else:
            inp = (10, 10)
            while inp[0] != game.get_must_move_board():
                print ('you can move in the board', game.get_must_move_board())
                inp = input('please move')
                inp = eval(inp)
        game.next_step(side, inp)
        side = -1 * side
    print (BetterNormalGame.convert_side_int_to_str(game.determineWinner()))

if __name__ == "__main__":
    new_game()
