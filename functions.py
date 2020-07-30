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
        # Neeed to update to deal one card to a player for 2 rounds
        df = pd.DataFrame()
        for x in range(players + 1):
            if x == players:
                stin = 'Dealer'
            else:
                stin = 'Player_' + str(x + 1)
            df.insert(x, stin, [self.cards.pop(0), self.cards.pop(0)])
        return df
    def blackjack(self, players, hit):
        # Could update for counting cards and changing the hit based on what card goes up for the dealer
        df = self.black_deal(players)
        for x in range(players + 1):
            if x == players:
                col = 'Dealer'
                hit = 16
            else:
                col = 'Player_' + str(x+1)
                if col != 'Player_1':
                    # Could update this to have a better chance to hit median (use random distribution)
                    hit = random.randint(13, 21)
            count = 2
            while np.nansum(df[col]) < hit:
                df.loc[count, col] = self.cards.pop(0)
                count += 1
        return self.black_check(df)
    def black_check(self,df):
        idf = pd.DataFrame(columns = list(df))
        for col in list(df):
            if np.nansum(df[col]) <= 21:
                idf.loc[0, col] = np.nansum(df[col])
            else:
                idf.loc[0, col] = 'Bust'
        #Putting ties as loses for now, will update with tie condition latter
        if idf.loc[0, 'Player_1'] == 'Bust':
            return 'Lose'
        elif idf.loc[0, 'Dealer'] == 'Bust':
            return 'Win'
        elif idf.loc[0, 'Player_1'] <= idf.loc[0, 'Dealer']:
            return 'Lose'
        else:
            return 'Win'
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
print(playing_cards().blackjack(1,16))