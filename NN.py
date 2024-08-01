
import NNBlackjack as BJ

import neat

import torch
from torch import nn
from torch import optim

class BlackjackModel(nn.Module):
    def __init__(self):
        super(BlackjackModel, self).__init__()
        self.fc1 = nn.Linear(2, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 2)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x


