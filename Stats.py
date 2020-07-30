import time
import functions as func
def black_stats(players, hit):
    stats = []
    for x in range(10000):
        stats.append(func.playing_cards().blackjack(players, hit))
    win = stats.count('Win')
    lose = stats.count('Lose')
    return win / (win + lose)
def loop_hit(players):
    hit = {}
    for i in range(13,22):
        # print('Stop hitting at:', i)
        x = black_stats(players, i)
        hit[i] = x
        # print(x)
    print('Results for', players, 'players:')
    print('Stop hitting at', max(hit, key = hit.get))
    print('This method has a', hit.get(max(hit, key=hit.get)) * 100, '% chance of success.')
def loop_players():
    for i in range(1,7):
        print('Players:',i)
        x = loop_hit(i)
        print(x)

start_time = time.time()
print(loop_players())
print("%s seconds" % (time.time() - start_time))