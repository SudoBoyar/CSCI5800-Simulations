from datetime import timedelta


def seconds(n):
    return n


def minutes(n):
    return n * 60


def hours(n):
    return n * 60 * 60


def days(n):
    return n * 60 * 60 * 24


def pretty_time(t):
    delta = timedelta(seconds=t)
    return str(delta)
