import os
import pygame

from math import floor
from controller import Controller
from QLearner import QNetwork
from engine import Tetris


def play(single_player=True, debug=False):
    if single_player:
        game = Controller(Tetris())
        player = QNetwork(gamma=1, model_path='models/model_balanced.h5')
        player.load_model()
        terminate = False
        pause = False

        states = game.reset()
        if debug:
            while not terminate:
                move, _ = player.get_state_with_move(states)
                states, _, terminate, _ = game.advance(move)

                print(game.render(debug=debug))
                os.system('cls')
        else:
            while not terminate:
                move, _ = player.get_state_with_move(states)
                if not pause:
                    states, _, terminate, _ = game.advance(move)

                game.render(debug=debug)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            pause = not pause
                        elif event.key == pygame.K_r:
                            game.reset()
    else:
        columns, rows = 10, 20
        game1 = Controller(Tetris(columns, rows))
        player_min = QNetwork(gamma=1, model_path='models/model_balanced.h5')
        player_min.load_model()

        game2 = Controller(Tetris(columns, rows))
        player_max = QNetwork(gamma=1, model_path='models/model_aggressive.h5')
        player_max.load_model()

        states1 = game1.reset()
        states2 = game2.reset()

        winner = False
        playing = True
        tie = False
        level = 0
        while playing:
            move1, _ = player_min.get_state_with_move(states1)
            states1, _, _, cleared1 = game1.advance(move1)

            move2, _ = player_max.get_state_with_move(states2)
            states2, _, _, cleared2 = game2.advance(move2)

            level += floor(cleared2/2) - floor(cleared1/2)

            os.system('cls')
            print(game1.render(debug=True))
            print(game2.render(debug=True))
            print("\nRow Difference: " + str(level))

            if abs(level) > floor(rows/2):
                winner = True

            playing = (not game1.delegate.is_game_over()) and (not game2.delegate.is_game_over()) and not winner
            add_level_to_state(states1, False, level)
            add_level_to_state(states2, True, level)

            if game1.delegate.is_game_over() and game2.delegate.is_game_over():
                tie = True
                break

        if tie:
            print("Both Players game overed at the same time.")
        elif game1.delegate.is_game_over() or game2.delegate.is_game_over():
            print("\n----------------------------------------\n"
                  "Player {} wins by game over.".format(str(int(game1.delegate.is_game_over()) + 1)))
        else:
            print("\n----------------------------------------\n"
                  "Player {} wins by {} line(s)!".format(str(int(level > 0) + 1), level - 10))


# Used to simulate row insertion.
def add_level_to_state(states, max_player, level):
    if level > 0 and not max_player:
        for state in states:
            state[1][3] += level
    elif level < 0 and max_player:
        for state in states:
            state[1][3] += abs(level)

if __name__ == '__main__':
    play(single_player=True)
