# This file is placed in the Public Domain.
#
# pylint: disable=R0903,W0105,E1102


"utilities"


from .thread import Errors, tostr


class Debug:

    "Debug"

    filter = []
    out = None


def debug(txt):
    "print to console."
    for skp in Debug.filter:
        if skp in txt:
            return
    Debug.out(txt)


def enable(func):
    "set output function."
    Debug.out = func


def errors():
    "show exceptions"
    for exc in Errors.errors:
        out(exc)


def out(exc):
    "check if output function is set."
    txt = str(tostr(exc))
    if Debug.out:
        Debug.out(txt)


"interface"


def __dir__():
    return (
        'debug',
        'enable',
        'errors',
        'out'
    )
