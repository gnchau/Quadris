from random import random
from engine import Tetris
from controller import Controller
from QLearner import QNetwork
from experiences import Experiences

reward_maps = {
    "balanced": {
        0: 1,
        1: 10,
        2: 40,
        3: 90,
        4: 160,
    },

    "aggressive": {
        0: 1,
        1: 10,
        2: 40,
        3: 90,
        4: 200,
    },

    "hyper aggressive": {
        0: 1,
        1: 10,
        2: 40,
        3: 90,
        4: 260,
    },
}


def run(engine: Tetris,
        learner: QNetwork,
        scores_name,
        length_name,
        initial_epsilon=1.0,
        final_epsilon=0,
        epsilon_stop_episode=1700,
        epsilon_checkpoint=False,
        batch_size=512,
        reward_map=None,
        model_path=None,
        episodes=2000):
    max_reward = 0
    if reward_map is None:
        reward_map = reward_maps["balanced"]
    if model_path is None:
        model_path = 'models/model.h5'
    if epsilon_checkpoint:
        f = open("./training_tools/checkpoints.txt", 'r')
        max_reward = int(f.read())
        f = open("./training_tools/epsilon_checkpoint.txt", 'r')
        initial_epsilon = float(f.read())

    experiences = Experiences(20000)
    controller = Controller(engine, reward_map=reward_map)

    for episode in range(episodes):
        current = controller.reset()
        previous_props = engine.get_properties([])
        terminal = False

        epsilon = final_epsilon + (max(epsilon_stop_episode - episode, 0)
                                   * (initial_epsilon - final_epsilon) /
                                   epsilon_stop_episode)

        while not terminal:
            will_explore = random() <= epsilon

            best_action, best_properties = learner.get_state_with_move(current, will_explore=will_explore)
            current, reward, terminal, _ = controller.advance(best_action)
            experiences.save_memory((previous_props, best_action, best_properties, reward, terminal))
            previous_props = best_properties

        batch = experiences.sample(batch_size=batch_size)
        learner.learn(batch, batch_size, len(experiences.memories), epochs=1)

        f = open(scores_name, 'a+')
        f.write(str(episode) + " " + str(controller.total_reward) + "\n")
        f.close()

        f = open(length_name, 'a+')
        f.write(str(episode) + " " + str(controller.length) + "\n")
        f.close()

        f = open("./training_tools/epsilon_checkpoint.txt", "w")
        f.write(str(epsilon))
        f.close()

        print("Game: {}  Length:{}  Reward: {}  Epsilon: {:.4f} Max Reward: {}"
              .format(episode + 1, controller.length,
                      controller.total_reward, epsilon, max_reward))

        if controller.total_reward >= max_reward:
            max_reward = controller.total_reward
            f = open("./training_tools/score_checkpoint.txt", "w")
            f.write(str(max_reward))
            f.close()
            learner.model.save(model_path)

        controller.reset_reward()


if __name__ == "__main__":
    run(Tetris(), QNetwork(), "./analysis/scores.txt", "./analysis/length.txt")
