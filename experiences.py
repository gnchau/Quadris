from collections import deque
from random import sample


class Experiences:
    """Represents an experience buffer of max length size"""
    def __init__(self, size=20000):
        self.memories = deque(maxlen=size)
        self.size = 0

    def save_memory(self, experience):
        """Experiences are of the form [previous state, reward, state, done]"""
        self.memories.append(experience)
        self.size += 1

    def sample(self, batch_size):
        if len(self.memories) < batch_size:
            return
        return sample(self.memories, batch_size)
