import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from controller import Controller
from QLearner import QNetwork
from engine import Tetris


def graph_frequencies(models, names, game_length=300):
    frequencies = get_data(models, game_length)

    df = pd.DataFrame([frequencies[0], frequencies[1], frequencies[2]], index=names).transpose()

    fig, ax = plt.subplots(1, 1, figsize=(6, 5))

    df.plot.bar(ax=ax)
    ax.set_xlabel('n')
    ax.set_ylabel('Frequency of n Cleared Lines in One Move Over the in a Game')
    plt.title('Models and The Frequency of Clearing n Lines for n = 1, 2, 3, 4')

    plt.tight_layout()
    plt.show()


def get_data(models, length):
    frequencies = []
    for model in models:
        frequency_for_game = []
        game = Controller(Tetris())
        player = QNetwork(gamma=1, model_path=model)
        player.load_model()
        end = False
        iteration = 0

        states = game.reset()
        while not end and iteration < length:
            move, _ = player.get_state_with_move(states)
            states, _, terminal, lines = game.advance(move)
            frequency_for_game.append(lines)
            if terminal:
                if len(frequency_for_game) == length:
                    end = True
                elif len(frequency_for_game) < length:
                    states = game.reset()
                    frequency_for_game.clear()
                    iteration = -1

            iteration += 1

        frequencies.append(filter(lambda x: x != 0, frequency_for_game))
    return [dict(Counter(freq)) for freq in frequencies]


if __name__ == '__main__':
    graph_frequencies(['models/model_balanced.h5', 'models/model_aggressive.h5', 'models/model_hyperaggressive.h5'],
                      ['Balanced', 'Aggressive', 'Hyper Agressive'], 300)
