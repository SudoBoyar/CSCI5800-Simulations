from datetime import timedelta


def seconds(n):
    return n


def minutes(n):
    return n * seconds(60)


def hours(n):
    return n * minutes(60)


def days(n):
    return n * hours(24)


def years(n):
    return n * days(365.25)


def pretty_time(t):
    delta = timedelta(seconds=t)
    return str(delta)
