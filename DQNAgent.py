import random

import torch.nn as nn
import torch

from ReplayBuffer import ReplayBuffer


class DQNAgent:
    def __init__(self, N=3, gamma=0.99, lr=1e-3, batch_size=64):
        self.N = N
        self.gamma = gamma
        self.batch_size = batch_size
        self.epsilon = 0.5  # hoch starten
        self.epsilon_min = 0.3
        self.epsilon_decay = 0.995

        self.model = nn.Sequential(
            nn.Linear(N * N, 128),
            nn.ReLU(),
            nn.Linear(128, 4)
        )
        self.target_model = nn.Sequential(
            nn.Linear(N * N, 128),
            nn.ReLU(),
            nn.Linear(128, 4)
        )
        self.target_model.load_state_dict(self.model.state_dict())

        self.optim = torch.optim.Adam(self.model.parameters(), lr=lr)
        self.loss_fn = nn.MSELoss()
        self.buffer = ReplayBuffer(5000)
        self.update_target_every = 50
        self.step_counter = 0

    def act(self, state, legal_mask):
        if random.random() < self.epsilon:
            legal = [i for i, m in enumerate(legal_mask) if m]
            return random.choice(legal)
        s = torch.tensor(state, dtype=torch.float32)
        q = self.model(s)
        q[torch.tensor(legal_mask) == 0] = -1e9
        return torch.argmax(q).item()

    def push(self, s, a, r, s_next, done):
        self.buffer.push(s, a, r, s_next, done)

    def train(self):
        if len(self.buffer) < self.batch_size:
            return

        s, a, r, s_next, done = self.buffer.sample(self.batch_size)

        q = self.model(s)
        q_a = q.gather(1, a.unsqueeze(1)).squeeze(1)

        with torch.no_grad():
            q_next = self.target_model(s_next).max(1)[0]
            target = r + self.gamma * q_next * (1 - done)

        loss = self.loss_fn(q_a, target)
        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

        self.step_counter += 1
        if self.step_counter % self.update_target_every == 0:
            self.target_model.load_state_dict(self.model.state_dict())

        # ε decay
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
