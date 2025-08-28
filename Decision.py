import os
import pickle

# CUSTOM INPUTS
PLAYER_TOTAL= 16
NUM_CARDS= 2
DEALER_CARD= 10
USABLE_ACE= 0

def load_winner_net():
    # Try to load the pickled network; if not available, rebuild from genome+config.
    try:
        with open('winner_net.pkl', 'rb') as f:
            return pickle.load(f)
    except Exception:
        # Fallback: rebuild the net from the pickled genome + config file.
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'config-feedforward.txt')
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    config_path)
        with open('winner_genome.pkl', 'rb') as f:
            winner_genome = pickle.load(f)
        return neat.nn.FeedForwardNetwork.create(winner_genome, config)

def decide_action_from_features(net, player_total, num_cards, dealer_visible_card, usable_ace):
    inputs = [
        player_total / 21.0,
        float(num_cards),
        dealer_visible_card / 11.0,
        float(usable_ace),
    ]
    return net.activate(inputs)[0]


# Example usage:
if __name__ == '__main__':
    net = load_winner_net()

    action = decide_action_from_features(net, player_total=PLAYER_TOTAL, num_cards=NUM_CARDS,
                                         dealer_visible_card=DEALER_CARD, usable_ace=USABLE_ACE)
    if action > 0.5:
        decision = 'Hit'
    else:
        decision = 'Stay'
    print('Decision:', decision,  '\nWith a confidence of : %', abs(action - 0.5) * 200, '\n',action)
