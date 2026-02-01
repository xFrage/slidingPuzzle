from Board import Board
from DQNAgent import DQNAgent

import logging
import torch

board = Board(3)
agent = DQNAgent(3)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger()


def main():
    for episode in range(1000):
        state = board.reset()
        done = False

        steps = 0
        total_reward = 0.0

        MAX_STEPS = 200

        while not done and steps < MAX_STEPS:
            mask = board.get_legal_mask()
            action = agent.act(state, mask)

            next_state, reward, done = board.step(action)
            agent.train(state, action, reward, next_state, done)

            state = next_state
            total_reward += reward
            steps += 1

        print(
            f"episode {episode:4d} | "
            f"steps {steps:3d} | "
            f"reward {total_reward:6.2f} | "
            f"solved {done}"
        )

    torch.save(agent.model.state_dict(), "dqn.pt")
    print("saved dqn model successfully!")


if __name__ == "__main__":
    main()
