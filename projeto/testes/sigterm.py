#! /usr/bin/env python

import signal


def ctrl_handler(signum, frm):
    print (f"Signal: {signum}")
    exit()

print ("Installing signal handler...")
signal.signal(signal.SIGINT, ctrl_handler)
print ("done")

while True:
    try:
    # do something
    except EOFError: