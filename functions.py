import pandas as pd
import random
import numpy as np


class playing_cards():
    def __init__(self):
        # Putting Aces as 11 for now
        self.cards = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8,
                      8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
                      10, 10, 10, 10, 10, 10, 11, 11, 11, 11]
        random.shuffle(self.cards)
        self.df = pd.DataFrame()


    def black_deal(self, players):
        for x in range(players + 1):
            if x == players:
                play = 'Dealer'
            else:
                play = 'Player_' + str(x + 1)
            self.df.insert(x, play, [self.cards.pop(0)])
        for col in list(self.df):
            self.df.loc[1, col] = self.cards.pop(0)

    def blackjack(self, players, hit):
        # Could update for counting cards and changing the hit based on what card goes up for the dealer
        self.black_deal(players)
        for x in range(players + 1):
            if x == players:
                col = 'Dealer'
                hit = 17
            else:
                col = 'Player_' + str(x + 1)
                if col != 'Player_1':
                    # Could update this to have a better chance to hit median (use normal distribution)
                    hit = random.randint(13, 21)
            self.black_ace(col)
            count = 2
            while np.nansum(self.df[col]) < hit:
                self.df.loc[count, col] = self.cards.pop(0)
                self.black_ace(col)
                count += 1
        return self.black_check()

    def black_check(self):
        idf = pd.DataFrame(columns=list(self.df))
        for col in list(self.df):
            if np.nansum(self.df[col]) <= 21:
                idf.loc[0, col] = np.nansum(self.df[col])
            else:
                idf.loc[0, col] = 'Bust'
        if idf.loc[0, 'Player_1'] == 'Bust':
            return 'Lose'
        elif idf.loc[0, 'Dealer'] == 'Bust':
            return 'Win'
        elif idf.loc[0, 'Player_1'] < idf.loc[0, 'Dealer']:
            return 'Lose'
        elif idf.loc[0, 'Player_1'] > idf.loc[0, 'Dealer']:
            return 'Win'
        else:
            return 'Tie'


    def black_ace(self, col):
        count = 0
        while 11 in self.df[col].unique() and np.nansum(self.df[col]) > 21:
            if self.df.loc[count, col] == 11:
                self.df.loc[count, col] = 1
            count += 1
