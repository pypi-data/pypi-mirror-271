# This file is placed in the Public Domain.
#
# pylint: disable=W0105


"runtime"


import time


from .broker import Broker


broker  = Broker()
dte     = time.ctime(time.time()).replace("  ", " ")


"interface"


def __dir__():
    return (
        'broker',
        'dte'
    )
