from collections import Counter
import random


class Dice(object):
    def __init__(self, nsides=6, ndice=2, distribution=None, seed=1):
        self.nsides = nsides
        self.ndice = ndice
        self.distribution = distribution if distribution is not None else [1] * nsides
        self.rand = random.Random(seed)

        self.dice_rolls = []
        self.rolls = []

    def roll(self):
        roll = self.rand.choices(range(1, self.nsides+1), weights=self.distribution, k=self.ndice)

        for die in roll:
            self.dice_rolls.append(die)
        self.rolls.append(sum(roll))

        return Roll(*roll)


class Roll(object):
    def __init__(self, *dice):
        if len(dice) > 0:
            self.roll = sorted(dice)
            self.total = sum(dice)
        else:
            raise Exception('Invalid Roll')

    def __eq__(self, other):
        return self.roll == other.roll

    def __str__(self):
        return "Roll(" + ', '.join(map(str, self.roll)) + ")"

    def __iter__(self):
        return iter(self.roll)


if __name__ == '__main__':
    d = Dice()
    print(d.roll())
    print(d.roll())

    d2 = Dice(ndice=1000000, distribution=[2, 2, 3, 1, 2, 2])
    r = d2.roll()

    c = Counter(r)
    print(c)
