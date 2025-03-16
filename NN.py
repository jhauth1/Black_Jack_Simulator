import pandas as pd
import random
import numpy as np
import neat
import os
import pickle
import visualize
GAMES = 10000
GENERATIONS = 10

class playing_cards():
    def __init__(self):
        # Initialize a deck of cards
        self.cards = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5,
                      6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9,
                      10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
                      10, 10, 10, 10, 10, 10, 11, 11, 11, 11]
        random.shuffle(self.cards)
        self.df = pd.DataFrame()
        self.game_data = []

    def black_deal(self, players):
        # Deal initial two cards to each player and dealer
        for x in range(players + 1):
            if x == players:
                play = 'Dealer'
            else:
                play = 'Player_' + str(x + 1)
            self.df.insert(x, play, [self.cards.pop(0)])
        for col in list(self.df):
            self.df.loc[1, col] = self.cards.pop(0)

    def black_ace(self, col):
        # Adjust for aces if total exceeds 21
        count = 0
        while 11 in self.df[col].unique() and np.nansum(self.df[col]) > 21:
            if self.df.loc[count, col] == 11:
                self.df.loc[count, col] = 1
            count += 1



def play_game_with_net(net):
    # Initialize a new game
    game = playing_cards()
    game.black_deal(players=1)

    # Player's initial hand
    player_hand = game.df['Player_1'].dropna()
    player_total = np.nansum(player_hand)
    dealer_visible_card = game.df.loc[0, 'Dealer']

    # Check for player's blackjack
    if player_total == 21 and len(player_hand) == 2:
        player_blackjack = True
    else:
        player_blackjack = False

    # Player's turn
    if not player_blackjack:
        while True:
            usable_ace = 0
            # Prepare inputs for the neural network
            if 11 in player_hand.values and player_total <= 21:
                usable_ace = 1
            num_cards= len(player_hand)

            inputs = [player_total / 21,num_cards,dealer_visible_card / 11, usable_ace]

            output = net.activate(inputs)

            # Decide whether to hit or stay
            if output[0] > 0.5:
                # Hit
                next_card = game.cards.pop(0)
                game.df.loc[len(game.df['Player_1'].dropna()), 'Player_1'] = next_card
                game.black_ace('Player_1')
                player_hand = game.df['Player_1'].dropna()
                player_total = np.nansum(player_hand)
                if player_total > 21:
                    return -1  # Player busts
            else:
                # Stay
                break

    # Dealer's turn
    dealer_hand = game.df['Dealer'].dropna()
    dealer_total = np.nansum(dealer_hand)
    if dealer_total == 21 and len(dealer_hand) == 2:
        dealer_blackjack = True
    else:
        dealer_blackjack = False

    if dealer_blackjack:
        if player_blackjack:
            return 0  # Tie
        else:
            return -1  # Dealer wins
    else:
        if player_blackjack:
            return 1  # Player wins
        else:
            while dealer_total < 17:
                game.df.loc[len(game.df['Dealer'].dropna()), 'Dealer'] = game.cards.pop(0)
                game.black_ace('Dealer')
                dealer_hand = game.df['Dealer'].dropna()
                dealer_total = np.nansum(dealer_hand)
            if dealer_total > 21:
                return 1  # Dealer busts, player wins
            else:
                if player_total > dealer_total:
                    return 1  # Player wins
                elif player_total < dealer_total:
                    return -1  # Dealer wins
                else:
                    return 0  # Tie

def eval_genomes(genomes, config):
    # Evaluate each genome
    for genome_id, genome in genomes:
        genome.fitness = 0.0  # Initialize fitness
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        for _ in range(GAMES):
            result = play_game_with_net(net)
            if result == 1:
                genome.fitness += 1  # Win
            elif result == -1:
                genome.fitness -= 1  # Loss
            else:
                genome.fitness += 0.0  # Tie

def run_neat():
    # Load configuration
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    # Create the population
    p = neat.Population(config)
    # Add reporters
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # Run NEAT
    winner = p.run(eval_genomes, GENERATIONS)
    # Show the winning genome
    print('\nBest genome:\n{!s}'.format(winner))
    return winner, config

if __name__ == '__main__':
    # Run NEAT and get the winner along with config
    winner, config = run_neat()

    # Visualize the winning genome's network architecture
    visualize.draw_net(config, winner, view=True, filename="winner_net")

    # Create the neural network from the winning genome
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    # Attempt to pickle the neural network; if that fails, pickle the genome instead.
    try:
        with open('winner_net.pkl', 'wb') as f:
            pickle.dump(winner_net, f)
        print("Neural network successfully pickled.")
    except Exception as e:
        print("Pickling network failed:", e)
        print("Pickling genome instead.")
        with open('winner_genome.pkl', 'wb') as f:
            pickle.dump(winner, f)
        print("Genome successfully pickled.")

    # Test the network
    test_wins = 0
    test_games = 999999
    for _ in range(test_games):
        result = play_game_with_net(winner_net)
        if result == 1:
            test_wins += 1
    print(f'\nTested the winning network over {test_games} games, won {test_wins} times.')
