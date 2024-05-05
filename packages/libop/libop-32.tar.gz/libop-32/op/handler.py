# This file is placed in the Public Domain.
#
# pylint: disable=R0903,W0105,W0212,W0718


"handler"


import inspect
import queue
import threading
import _thread


from .objects import Default, Object
from .threads import later, launch


class Handler:

    "Handler"

    def __init__(self):
        self.cbs      = Object()
        self.queue    = queue.Queue()
        self.stopped  = threading.Event()
        self.threaded = True

    def callback(self, evt):
        "call callback based on event type."
        func = getattr(self.cbs, evt.type, None)
        if not func:
            evt.ready()
            return
        evt._thr = launch(func, self, evt)

    def loop(self):
        "proces events until interrupted."
        while not self.stopped.is_set():
            try:
                evt = self.poll()
                self.callback(evt)
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    def poll(self):
        "function to return event."
        return self.queue.get()

    def put(self, evt):
        "put event into the queue."
        self.queue.put_nowait(evt)

    def register(self, typ, cbs):
        "register callback for a type."
        setattr(self.cbs, typ, cbs)

    def start(self):
        "start the event loop."
        launch(self.loop)

    def stop(self):
        "stop the event loop."
        self.stopped.set()


class Client(Handler):

    "Client"

    def __init__(self):
        Handler.__init__(self)
        self.register("command", command)

    def announce(self, txt):
        "announce text."
        self.raw(txt)

    def raw(self, txt):
        "raw output."

    def say(self, _channel, txt):
        "say text in a channel."
        self.raw(txt)

    def show(self, evt):
        "show results into a channel."
        for txt in evt.result:
            self.say(evt.channel, txt)


"command"


class Command(Object):

    "Command"

    cmds = Object()


def add(func):
    "add command."
    setattr(Command.cmds, func.__name__, func)


def command(bot, evt):
    "check for and run a command."
    parse_cmd(evt)
    func = getattr(Command.cmds, evt.cmd, None)
    if func:
        try:
            func(evt)
        except Exception as exc:
            later(exc)
    bot.show(evt)
    evt.ready()


"utilities"


def parse_cmd(obj, txt=None):
    "parse a string for a command."
    args = []
    obj.args    = obj.args or []
    obj.cmd     = obj.cmd or ""
    obj.gets    = obj.gets or Default()
    obj.hasmods = obj.hasmod or False
    obj.index   = None
    obj.mod     = obj.mod or ""
    obj.opts    = obj.opts or ""
    obj.result  = obj.reult or []
    obj.sets    = obj.sets or Default()
    obj.txt     = txt or obj.txt or ""
    obj.otxt    = obj.txt
    _nr = -1
    for spli in obj.otxt.split():
        if spli.startswith("-"):
            try:
                obj.index = int(spli[1:])
            except ValueError:
                obj.opts += spli[1:]
            continue
        if "==" in spli:
            key, value = spli.split("==", maxsplit=1)
            if key in obj.gets:
                val = getattr(obj.gets, key)
                value = val + "," + value
            setattr(obj.gets, key, value)
            continue
        if "=" in spli:
            key, value = spli.split("=", maxsplit=1)
            if key == "mod":
                obj.hasmods = True
                if obj.mod:
                    obj.mod += f",{value}"
                else:
                    obj.mod = value
                continue
            setattr(obj.sets, key, value)
            continue
        _nr += 1
        if _nr == 0:
            obj.cmd = spli
            continue
        args.append(spli)
    if args:
        obj.args = args
        obj.txt  = obj.cmd or ""
        obj.rest = " ".join(obj.args)
        obj.txt  = obj.cmd + " " + obj.rest
    else:
        obj.txt = obj.cmd or ""


def scancmd(mod) -> None:
    "scan module for commands."
    for key, cmd in inspect.getmembers(mod, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in cmd.__code__.co_varnames:
            add(cmd)


"interface"


def __dir__():
    return (
        'Client',
        'Commands',
        'Handler',
        'add',
        'command',
        'parse_cmd',
    )
