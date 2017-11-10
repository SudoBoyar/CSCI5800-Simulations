import abc
import random


class DistributionGenerator(metaclass=abc.ABCMeta):
    def __init__(self, total=None, seed=0, source=None):
        self.index = total
        self.source = source if isinstance(source, random.Random) else random.Random(seed)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index is not None:
            if self.index == 0:
                raise StopIteration

            self.index -= 1

        return self.next()

    @abc.abstractmethod
    def next(self):
        pass

    def getlist(self, count=1):
        return [self.__next__() for _ in range(count)]


class Exponential(DistributionGenerator):
    def __init__(self, lambd, total=None, seed=222, source=None):
        super().__init__(total, seed, source)
        self.lambd = lambd

    def next(self):
        return self.source.expovariate(self.lambd)


class Flat(DistributionGenerator):
    def __init__(self, a, b, total=None, seed=333, source=None):
        super().__init__(total, seed, source)
        self.a = a
        self.b = b

    def next(self):
        return self.source.uniform(self.a, self.b)


class Normal(DistributionGenerator):
    def __init__(self, mu, sigma, total=None, seed=111, source=None):
        super().__init__(total, seed, source)
        self.mu = mu
        self.sigma = sigma

    def next(self):
        return self.source.normalvariate(self.mu, self.sigma)


if __name__ == '__main__':
    exp = Flat(1, 6, 10)
    print(exp.getlist(2))
    for i in exp:
        print(i)

