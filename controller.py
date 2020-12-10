from numpy import array
import pygame

from engine import Tetris
from visual_view import Visual


class Controller:
    """
    Used to represent the game values and stores the reward information for the learner.
    """
    def __init__(self, delegate: Tetris, reward_map=None):
        self.delegate = delegate
        self.length = 0
        self.total_reward = 0
        if reward_map is None:
            reward_map = {
                0: 0,
                1: 10,
                2: 40,
                3: 90,
                4: 160,
            }
        self.reward_map = reward_map

    def reset(self):
        self.delegate = Tetris()
        self.length = 0
        return array(self.delegate.generate_possible_states(), dtype="object")

    def advance(self, action):
        """Performs one step/frame in the game and returns the observation, reward and if the game is over."""
        self.length += 1
        x, rotation = action
        self.delegate.combined_moves(x, rotation)

        rows = self.delegate.row_clean()
        rows_count = len(rows)
        terminal = self.delegate.is_game_over()

        reward = 1

        reward += self.reward_map[rows_count]

        if terminal:
            reward -= 2

        self.total_reward += reward

        return array(self.delegate.generate_possible_states(), dtype="object"), reward, terminal, rows_count

    def reset_reward(self):
        self.total_reward = 0

    def render(self, debug=False, width=450, height=550):
        if debug:
            return str(self.delegate) + "Score: " + str(self.delegate.score)
        else:
            pygame.init()
            visual_view = pygame.display.set_mode((width, height))
            pygame.display.set_caption("Quadris")
            display = Visual(self.delegate, visual_view)

            display.render()
            pass
