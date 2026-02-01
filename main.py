from Board import Board
from UI import UI
from DQNAgent import DQNAgent

import logging
import torch

trainingEpisodes = 100
MAX_STEPS = 50
BATCH_SIZE = 64
SHUFFLE_STEPS = 10

board = Board(3)
agent = DQNAgent(3, batch_size=BATCH_SIZE)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger()


def main():
    count = 0
    for episode in range(trainingEpisodes):

        state = board.reset(SHUFFLE_STEPS)
        done = False
        steps = 0
        total_reward = 0

        while not done and steps < MAX_STEPS:
            mask = board.get_legal_mask()
            action = agent.act(state, mask)
            next_state, reward, done = board.step(action)
            agent.push(state, action, reward, next_state, done)
            agent.train()
            state = next_state
            total_reward += reward
            steps += 1
        save_model()
        if done: count += 1
        success_ratio = count / (episode + 1) * 100
        print(
            f"Episode {episode:4d} | steps {steps:2d} | reward {total_reward:5.2f} | solved {done} | success {success_ratio:.1f}% | epsilon {agent.epsilon:.2f}")

    successRatio = (count * 100) / trainingEpisodes
    print("success ratio: ", successRatio, "%")


def save_model():
    torch.save(agent.model.state_dict(), "dqn.pt")


if __name__ == "__main__":
    main()
