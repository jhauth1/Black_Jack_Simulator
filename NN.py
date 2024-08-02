
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

def evaluate_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    game = playing_cards()
    game.blackjack(1, 17)  # Deal the initial cards
    player_cards = np.sum(game.df['Player_1'].dropna())
    dealer_card = game.df['Dealer'][0]
    input_data = torch.tensor([player_cards, dealer_card, 0])  # Assuming 0 for no hit/stay yet

    output = net.activate(input_data)
    decision = np.argmax(output)  # 0 for stay, 1 for hit
    return decision


