from collections import Counter
import distribution_generator as dg
import math
import matplotlib.pyplot as plt
import os
import simpy

from simtime import hours as simhours, minutes as simminutes
from dice import Dice
from game_stats import GameStats
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

    stats = {}
    for distr_name, distr in dice_distributions.items():
        print("Running ", distr_name)
        env = simpy.Environment()
        table = Table(env, Dice(distribution=distr))
        game_stats = GameStats(table)
        env.process(player_generator(env=env, table=table,
                                     arrival_dist=dg.Exponential(1 / simminutes(10)),
                                     play_time_dist=dg.Flat(simminutes(30), simhours(3)),
                                     # play_time_dist=dg.Normal(simhours(1.5), simminutes(45), minimum=30.0),
                                     wait_time_dist=dg.Flat(simminutes(2), simminutes(15)),
                                     num_players=100))
        env.run()

        directory = check_directory(distr_name)
        stats[distr_name] = game_stats.data()

        plot_rolls(table, directory)
        plot_stats(game_stats, directory)

    plot_all_stats(stats)


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


def check_directory(directory):
    result_dir = 'results/{0}'.format(directory)
    if not os.path.exists(result_dir):
        os.mkdir(result_dir, 0o755)
        os.chmod(result_dir, 0o755)

    return result_dir


def plot_rolls(table, directory):
    die_counter = Counter(table.dice.dice_rolls)
    roll_counter = Counter(table.dice.rolls)
    # print(die_counter)
    # print(roll_counter)
    # _, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    _, (ax1, ax2) = plt.subplots(1, 2)
    ax1.bar(list(die_counter.keys()), die_counter.values())
    ax1.xaxis.set_ticks(range(1, table.dice.nsides + 1))
    ax1.xaxis.set_ticklabels(range(1, table.dice.nsides + 1))
    ax2.bar(list(roll_counter.keys()), roll_counter.values())
    ax2.xaxis.set_ticks(range(2, table.dice.nsides * 2 + 1))
    ax2.xaxis.set_ticklabels(range(2, table.dice.nsides * 2 + 1))

    plt.savefig(os.path.join(directory, 'dice.png'), bbox_inches='tight')
    plt.savefig(os.path.join(directory, 'dice.pdf'))


def plot_stats(game_stats, directory):
    data = game_stats.data()
    print(list(data.keys()))
    print(data.values())
    fig, ax = plt.subplots()
    ax.bar(range(len(data)), data.values())
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(data.keys())

    plt.savefig(os.path.join(directory, 'game_stats.png'))
    plt.savefig(os.path.join(directory, 'game_stats.pdf'))


def plot_all_stats(stats):
    fig, axi = plt.subplots(2, int(math.ceil(len(stats) / 2)), sharey=True)

    axi[-1, -1].axis('off')

    # fig.set_dpi(200)
    fig.set_size_inches(10, 8)
    fig.subplots_adjust(hspace=.5)
    # fig.subplots_adjust(hspace=.75, wspace=.5)
    # fig.tight_layout()

    plt.xticks(rotation='vertical')
    # plt.margins(0.2)

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

    plots = []
    current = 0

    for label, game_stats in stats.items():
        ax = axi[0 if int(math.ceil(len(stats) / 2)) > current else 1][current % int(math.ceil(len(stats) / 2))]
        color = colors[current]
        current += 1

        plot = ax.bar(range(len(game_stats)), game_stats.values(), color=color)
        plots.append(plot)
        ax.set_xticks(range(len(game_stats)))
        ax.set_xticklabels(game_stats.keys(), ha='right')

        axlabels = ax.get_xticklabels()
        plt.setp(axlabels, rotation=45)
        # ax.set_xlabel(label)

        # labels = game_stats.keys()

    fig.legend(plots, stats.keys(), loc='lower right')
    plt.savefig('results/all_stats.png', bbox_inches='tight')


if __name__ == '__main__':
    run()
