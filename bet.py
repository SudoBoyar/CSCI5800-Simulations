from odds import *


class Bet(object):

    def __init__(self, table, name, true_odds, payout, winning_rolls=None, losing_rolls=None):
        self.table = table
        self.name = name
        self.true_odds = true_odds
        self.payout = payout
        self.winning_rolls = winning_rolls if winning_rolls is not None else []
        self.losing_rolls = losing_rolls if losing_rolls is not None else []
        self.paid = 0.0
        self.raked = 0.0

        self.hit = 0
        self.miss = 0
        self.hit_intervals = []
        self.since_last_hit = 0

    def handle_roll(self, roll):
        if not self.is_active():
            return

        if self.is_hit(roll):
            self.handle_hit(roll)
        else:
            if self.is_loss(roll):
                self.handle_loss(roll)
            self.handle_miss(roll)

    def is_hit(self, roll):
        for winner in self.winning_rolls:
            if roll == winner:
                return True

        return False

    def is_loss(self, roll):
        if self.is_hit(roll):
            # We're checking hits first, so this shouldn't be hit, but just in case, this allows for
            # simpler handling of bets like hardways, we can win on [[4,4]], and lose on [8], rather
            # than listing out all of the individual combinations that add up to 8 but aren't [4,4]
            return False

        for loss in self.losing_rolls:
            if roll == loss:
                return True

        return False

    def is_active(self):
        return True

    def handle_hit(self, roll):
        self.hit += 1
        self.hit_intervals.append(self.since_last_hit)
        self.since_last_hit = 0
        self.handle_payout(roll)

    def handle_payout(self, roll):
        self.paid += self.payout.amount(1.0)

    def handle_miss(self, roll):
        self.miss += 1
        self.since_last_hit += 1

    def handle_loss(self, roll):
        self.raked += 1.0


class SingleRoll(Bet):

    def is_loss(self, roll):
        return not self.is_hit(roll)


class PropBet(Bet):
    """
    One of the center table bets that isn't a single roll bet.
    """
    pass


class ComeOutBet(Bet):
    """
    A bet that is active before a point is set.
    """

    def is_active(self):
        return not self.table.has_point()


class PointBet(Bet):
    """
    A bet that is active after a point is set.
    """

    def is_active(self):
        return self.table.has_point()


class FieldBet(PointBet):
    def __init__(self, table):
        super(FieldBet, self).__init__(table, 'Field', Odds(5, 4), Payout(1, 1), [2, 3, 4, 9, 10, 11, 12], [5, 6, 7, 8])
        self.payout_2_12 = Payout(2, 1)

    def handle_payout(self, roll):
        if roll in [2, 12]:
            self.paid += self.payout_2_12.amount(1.0)
        else:
            self.paid += self.payout(1.0)


class AllBet(PropBet):
    def __init__(self, table):
        super(AllBet, self).__init__(table, "Make 'em all", Odds(190, 1), Payout(175, 1), losing_rolls=[7])
        self.seen = [False for _ in range(13)]
        self.required = [i not in (0, 1, 7) for i in range(13)]

    def is_hit(self, roll):
        self.seen[roll.total] = True
        return self.seen == self.required

    def handle_hit(self, roll):
        super(AllBet, self).handle_hit(roll)
        self.seen = [False for _ in range(13)]


class TallBet(PropBet):
    def __init__(self, table):
        super(TallBet, self).__init__(table, "All Tall", Odds(190, 1), Payout(175, 1), losing_rolls=[7])
        self.seen = [False for _ in range(8, 13)]

    def is_hit(self, roll):
        if roll <= 7:
            return False
        self.seen[roll.total - 8] = True
        return all(self.seen)

    def handle_hit(self, roll):
        super(TallBet, self).handle_hit(roll)
        self.seen = [False for _ in range(8, 13)]


class SmallBet(PropBet):
    def __init__(self, table):
        super(SmallBet, self).__init__(table, "All Small", Odds(190, 1), Payout(175, 1), losing_rolls=[7])
        self.seen = [False for _ in range(2, 7)]

    def is_hit(self, roll):
        if roll >= 7:
            return False
        self.seen[roll.total - 2] = True
        return all(self.seen)

    def handle_hit(self, roll):
        super(SmallBet, self).handle_hit(roll)
        self.seen = [False for _ in range(2, 7)]
