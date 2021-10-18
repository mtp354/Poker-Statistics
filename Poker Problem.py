# A poker simulation problem

import numpy as np
from numpy import random
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

# After N rounds of poker by k players, starting with C0 chips, how many players are expected to have more
# chips than they started with?

C0 = 100  # The starting number of chips
k = 8  # Number of players
smallBlind = 1  # The value of the small blind
purseList = k*[C0]  # List of current purse amounts for each player
mu = 1  # Mean player bet size
sigma = 1  # Std. dev of player bet size


def number_ahead(players, starting_value=C0):
    n = 0
    for i in range(len(players)):
        if players[i] > starting_value:
            n = n + 1
    return n


def truncated_normal(mean, stddev, minval, maxval):
    return np.clip(np.random.normal(mean, stddev), minval, maxval)


def get_active_number(players):  # returns the number of players who are still in the game
    players_remaining = len([i for i, e in enumerate(players) if e != 0])
    return players_remaining


def player_loss(purse):  # A more sophisticated model of player betting behaviour as truncated normal distribution
    return round(truncated_normal(mu*smallBlind*k, stddev=sigma*k*smallBlind, minval=0, maxval=purse-smallBlind))


def pokerRound(players, blind=smallBlind):
    players_remaining = get_active_number(players)
    positions = list(range(len(players)))
    winnerPosition = np.random.choice(positions, p=[1/players_remaining if x != 0 else 0 for x in players])
    # now subtracting money from the losers
    winnings = (players_remaining-1)*blind
    for i in range(len(players)):
        if players[i] > 0 and i != winnerPosition:
            loss = player_loss(players[i])
            players[i] = players[i] - blind - loss
            winnings = winnings + loss
    for i in range(len(players)):
        if i == winnerPosition:
            players[i] = players[i] + winnings
    return


def tournament(players, blind=smallBlind):  # Simulates a game until one player has all of the available chips
    N = [0]
    while get_active_number(players) > 1:
        pokerRound(players)
        N.append(number_ahead(players))
        # print(purseList)
    return N


def get_convergence_round(listn):
    convergence_round = []
    for item in listn:
        convergence_round.append(len(item))
    return convergence_round


def sampler(players, iterations, mu_choice, sigma_choice, blind=smallBlind):
    mu = mu_choice
    sigma = sigma_choice
    N_list = []
    i = 1
    while i < iterations:
        player_list = players.copy()
        n = list(tournament(player_list))
        N_list.append(n)
        i += 1
    return N_list


mu_list = [x * 0.01 for x in range(10, 400)]
sigma_list = [x * 0.01 for x in range(10, 400)]

mega_list = []
for i in range(len(mu_list)):
    dummy_list = list(sampler(purseList, 500, mu_list[i], sigma_list[i]))
    mega_list.append(dummy_list)


# converge_data = get_convergence_round(testlist)
# num_bins = 200
# n, bins, patches = plt.hist(converge_data, num_bins, facecolor='blue', alpha=0.5)
# plt.show()



