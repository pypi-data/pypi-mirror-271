# This file is placed in the Public Domain.
#
# pylint: disable=W0105,W0718


"runtime"


import time


from .brokers import Broker
from .storage import scancls
from .message import Event
from .handler import Client, command, scancmd
from .threads import later
from .utility import spl


broker  = Broker()
dte     = time.ctime(time.time()).replace("  ", " ")


def cmnd(txt, outer):
    "do a command using the provided output function."
    clt = Client()
    clt.raw = outer
    evn = Event()
    evn.orig = object.__repr__(clt)
    evn.txt = txt
    command(clt, evn)
    evn.wait()
    return evn


def init(pkg, modstr, disable=""):
    "start modules"
    mds = []
    for modname in spl(modstr):
        if skip(modname, disable):
            continue
        mod = getattr(pkg, modname, None)
        if not mod:
            continue
        if "init" in dir(mod):
            try:
                mod.init()
                mds.append(mod)
            except Exception as ex:
                later(ex)
    return mds


def scan(pkg, modstr, disable=""):
    "scan modules for commands and classes"
    mds = []
    for modname in spl(modstr):
        if skip(modname, disable):
            continue
        module = getattr(pkg, modname, None)
        if not module:
            continue
        scancmd(module)
        scancls(module)
    return mds


def skip(name, skipp):
    "check for skipping"
    for skp in spl(skipp):
        if skp in name:
            return True
    return False


"interface"


def __dir__():
    return (
        'broker',
        'cmnd',
        'dte'
    )
