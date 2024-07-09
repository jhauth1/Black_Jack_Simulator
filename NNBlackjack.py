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
        # self.hitters = np.random.normal(17, 2, 2000)
        # self.hitters = [int(i) for i in self.hitters if i < 22 and i >= 13]
        # import matplotlib.pyplot as plt
        # count, bins, ignored = plt.hist(self.hitters, 30, density=True)
        # plt.plot(bins, 1 / (2 * np.sqrt(2 * np.pi)) *
        #          np.exp(- (bins - 17) ** 2 / (2 * 2 ** 2)),
        #          linewidth=2, color='r')
        # print('max:', max(self.hitters))
        # print('min:', min(self.hitters))
        # print('Count:', len(self.hitters))
        # plt.show()

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
        if hit > 21:
            hit = 21
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
            # self.black_ace(col)
            # count = 2
            while np.nansum(self.df[col]) < hit:
                self.df.loc[len(self.df[col].dropna()), col] = self.cards.pop(0)
                self.black_ace(col)
                # count += 1
        return self.black_check()

    def black_check(self):
        bust = -1
        tie = 0
        win = 1
        blackjack = 1.5
        idf = pd.DataFrame(columns=list(self.df))
        for col in list(self.df):
            if np.nansum(self.df[col]) <= 21:
                idf.loc[0, col] = np.nansum(self.df[col])
                idf.loc[1, col] = len(self.df[col].dropna())
            else:
                idf.loc[0, col] = 'Bust'
        if idf.loc[0, 'Player_1'] == 'Bust':
            return bust
        elif idf.loc[0, 'Player_1'] == 21 and idf.loc[1, 'Player_1'] == 2 and not (idf.loc[0, 'Dealer'] == 21 and idf.loc[1, 'Dealer'] == 2):
            return blackjack
        elif idf.loc[0, 'Dealer'] == 'Bust':
            return win
        elif idf.loc[0, 'Player_1'] < idf.loc[0, 'Dealer']:
            return bust
        elif idf.loc[0, 'Player_1'] > idf.loc[0, 'Dealer']:
            return win
        else:
            return tie
        # try:
        #     win = np.nanmax(idf)
        #     idf.loc[0] = idf.loc[0].fillna('Bust')
        #     if idf.loc[0,'Player_1'] >= idf.loc[0,'Player_1']:
        #         return 'Win'
        #     # elif idf.loc[0,'Player_1'] == 'Bust'
        #     #     return 'Bust'
        #     else:
        #         return 'Lose'
        # except:
        #     return 'Lose'
        # winners = []
        # for col in list(idf):
        #     if idf.loc[0, col] == win:
        #         winners.append(col)
        # print(idf)
        # print('Winner is', winners, 'with a score of', win)

    def black_ace(self, col):
        count = 0
        while 11 in self.df[col].unique() and np.nansum(self.df[col]) > 21:
            if self.df.loc[count, col] == 11:
                self.df.loc[count, col] = 1
            count += 1
