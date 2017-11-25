from collections import Counter
import distribution_generator as dg
import matplotlib.pyplot as plt
import os
import simpy

from simtime import hours as simhours, minutes as simminutes
from dice import Dice
from player import Player
from table import Table

env = None
dice_distributions = {
    'flat': [1, 1, 1, 1, 1, 1],
    'heavy_3': [1, 1, 2, 1, 1, 1],
    'very_heavy_3': [1, 1, 3, 1, 1, 1],
    'heavy_3_light_4': [2, 2, 3, 1, 2, 2],
    'very_heavy_3_light_4': [2, 2, 4, 1, 2, 2],
    'heavy_corner': [2, 2, 2, 1, 1, 1],
    'very_heavy_corner': [3, 3, 3, 1, 1, 1]
}


def run():
    global env

    for distr_name, distr in dice_distributions.items():
        print("Running ", distr_name)
        env = simpy.Environment()
        table = Table(env, Dice(distribution=distr))
        env.process(player_generator(env=env, table=table,
                                     arrival_dist=dg.Exponential(1/simminutes(10)),
                                     play_time_dist=dg.Flat(simminutes(30), simhours(3)),
                                     # play_time_dist=dg.Normal(simhours(1.5), simminutes(45), minimum=30.0),
                                     wait_time_dist=dg.Flat(simminutes(2), simminutes(15)),
                                     num_players=100))
        env.run()
        plot_rolls(table, distr_name)


def player_generator(env, table, arrival_dist, play_time_dist, wait_time_dist, num_players=None):
    current_id = 0
    for arrival in arrival_dist:
        if num_players is not None:
            if num_players == 0:
                raise StopIteration

            num_players -= 1

        player = Player(table, current_id, next(play_time_dist), next(wait_time_dist))
        current_id += 1

        yield env.timeout(arrival)
        env.process(player.arrive(env))


def plot_rolls(table, file_prefix=None):
    if not os.path.exists('results'):
        os.mkdir('results', 666)

    die_counter = Counter(table.dice.dice_rolls)
    roll_counter = Counter(table.dice.rolls)
    print(die_counter)
    print(roll_counter)
    # _, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    _, (ax1, ax2) = plt.subplots(1, 2)
    ax1.bar(list(die_counter.keys()), die_counter.values())
    ax1.xaxis.set_ticks(range(1, table.dice.nsides + 1), 1)
    ax2.bar(list(roll_counter.keys()), roll_counter.values())
    ax2.xaxis.set_ticks(range(2, table.dice.nsides * 2 + 1), 1)

    if file_prefix is None:
        file_prefix = ''
    elif file_prefix[-1] != '_':
        file_prefix = file_prefix + '_'

    plt.savefig('results/{prefix}dice.png'.format(prefix=file_prefix), bbox_inches='tight')
    plt.savefig('results/{prefix}dice.pdf'.format(prefix=file_prefix))


if __name__ == '__main__':
    run()
