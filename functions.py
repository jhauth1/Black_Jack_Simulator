import pandas as pd
import random
import numpy as np
class playing_cards():
    def __init__(self):
        # Putting Aces as 1 for now, put into 'A' when done
        self.cards = [2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,
                8,8,9,9,9,9,10,10,10,10,10,10,10,10,10,10,
                10,10,10,10,10,10,1,1,1,1]
        random.shuffle(self.cards)
    def black_deal(self,players):
        df = pd.DataFrame()
        for x in range(players + 1):
            if x == players:
                stin = 'Dealer'
            else:
                stin = 'Player_' + str(x + 1)
            df.insert(x, stin, [self.cards.pop(0),self.cards.pop(0)])
        return df
    def blackjack(self, players, hit):
        df = self.black_deal(players)
        for x in range(players + 1):
            if x == players:
                col = 'Dealer'
                hit = 16
            else:
                col = 'Player_' + str(x+1)
            count = 2
            while np.nansum(df[col]) < hit:
                df.loc[count, col] = self.cards.pop(0)
                count += 1
        return df
print(playing_cards().blackjack(5,16))