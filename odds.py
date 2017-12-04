
class Odds(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.fraction = float(b) / float(a+b)

    def __str__(self):
        return "%d:%d odds - %f.02%%".format(self.a, self.b, self.fraction)

    def __float__(self):
        return self.fraction

    def __eq__(self, other):
        if isinstance(other, Odds):
            return abs(self.fraction - other.fraction) < 1e-6
        else:
            return abs(self.fraction - float(other)) < 1e-6

    def even_payout(self):
        return Payout(self.b, self.a)

    def expected(self, events):
        return self.fraction * events


class Payout(Odds):
    def __str__(self):
        return "%d:%d payout".format(self.a, self.b)

    def __call__(self, *args, **kwargs):
        return self.amount(*args)

    def amount(self, bet):
        return bet * 1.0/self.fraction
