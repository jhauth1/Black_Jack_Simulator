import time
import functions as func
import math


def black_stats(players, hit):
    stats = []
    for x in range(10000):
        stats.append(func.playing_cards().blackjack(players, hit))
    return stats.count('Win') / len(stats)


def loop_hit(players):
    hit = {}
    for i in range(13, 22):
        # print('Stop hitting at:', i)
        x = black_stats(players, i)
        hit[i] = x
        # print(x)
    print('Stop hitting at', max(hit, key=hit.get))
    print('This method has a', hit.get(max(hit, key=hit.get)) * 100, '% chance of success.')


def loop_players():
    for i in range(1, 8):
        print('Players:', i)
        loop_hit(i)


start_time = time.time()
loop_hit(5)
time = (time.time() - start_time)
print()
if time < 60:
    print("Seconds: %s" % time)
elif time < (60*60):
    minutes = math.floor(time/60)
    print('Minutes: %s\nSeconds: %s ' % (minutes, (time - math.floor(minutes*60))))
else:
    hour = math.floor(time/(60*60))
    minutes = math.floor(time/60 - (hour*60))
    print('Hours: %s\nMinutes: %s\nSeconds: %s' %
          (hour, minutes, math.floor(time - (60*60*hour) - (minutes*60))))
