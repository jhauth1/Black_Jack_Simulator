import time
import NNBlackjack as BJ
import math
import gym
import numpy as np
import PIL.Image
import tensorflow as tf
import utils



from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.losses import MSE
from tensorflow.keras.optimizers import Adam

def create_model():
    model = Sequential()
    model.add(Dense(24, input_dim=2, activation='relu'))  # Adjust input_dim as needed
    model.add(Dense(24, activation='relu'))
    model.add(Dense(1, activation='linear'))
    model.compile(loss='mse', optimizer=Adam(learning_rate=0.001))
    return model

model = create_model()

def train_model(game_data, model):
    states = []
    targets = []
    for BJ.df, action, reward in game_data:
        state_values = [BJ.df['Player_1'].values(), BJ.df.loc[0, 'Dealer']]
        states.append(state_values)
        targets.append(reward)
    states = np.array(states)
    targets = np.array(targets)
    model.fit(states, targets, epochs=10, verbose=0)

train_model(game.game_data, model)

def choose_action(state, model):
    if np.random.rand() <= 0.1:  # Exploration
        return random.randint(13, 21)
    state_values = [sum(state['Player_1'].values()), sum(state['Dealer'].values())]
    q_values = model.predict(np.array([state_values]))
    return np.argmax(q_values[0])

for _ in range(1000):  # Play another 1000 games
    state = game.df.to_dict()
    action = choose_action(state, model)
    reward = game.blackjack(players=1, hit=action)
    game.game_data.append((state, action, reward))
    train_model(game.game_data, model)