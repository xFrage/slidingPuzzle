import torch
import torch.nn as nn
import random
import os


class DQNAgent:
    def __init__(self, size):
        self.model = nn.Sequential(
            nn.Linear(size * size, 128),
            nn.ReLU(),
            nn.Linear(128, 4)
        )

        if os.path.exists("dqn.pt"):
            print("loading dqn model...")
            self.model.load_state_dict(torch.load("dqn.pt"))
            print("done!")

        self.optim = torch.optim.Adam(self.model.parameters(), lr=1e-3)
        self.loss_fn = nn.MSELoss()
        self.gamma = 0.99
        self.epsilon = 0.1

    def act(self, state, legal_mask):
        if random.random() < self.epsilon:
            legal = [i for i, m in enumerate(legal_mask) if m]
            return random.choice(legal)

        with torch.no_grad():
            s = torch.tensor(state, dtype=torch.float32)
            q = self.model(s)
            q[torch.tensor(legal_mask) == 0] = -1e9
            return torch.argmax(q).item()

    def train(self, s, a, r, s_next, done):
        s = torch.tensor(s, dtype=torch.float32)
        s_next = torch.tensor(s_next, dtype=torch.float32)

        q = self.model(s)[a]

        with torch.no_grad():
            q_next = torch.max(self.model(s_next))
            target_value = r if done else r + self.gamma * q_next
            target = torch.tensor(target_value, dtype=torch.float32)

        loss = self.loss_fn(q, target)

        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

        return loss.item()
