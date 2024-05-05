# This file is placed in the Public Domain.
#
# pylint: disable=R0903,W0105,E1102


"logging"


class Logging:

    "Debug"

    filter = []
    out = None


def debug(txt):
    "print to console."
    for skp in Logging.filter:
        if skp in txt:
            return
    if Logging.out:
        Logging.out(txt)


def enable(func):
    "set output function."
    Logging.out = func


"interface"


def __dir__():
    return (
        'debug',
        'enable'
    )
