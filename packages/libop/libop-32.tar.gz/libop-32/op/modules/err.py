# This file is placed in the Public Domain.
#
# pylint: disable=W0622,E0402


"deferred exception handling"


from ..threads import Errors, format


def err(event):
    "show errors."
    nmr = 0
    event.reply(f"status: {nmr} errors: {len(Errors.errors)}")
    for exc in Errors.errors:
        txt = format(exc)
        for line in txt.split():
            event.reply(line)
