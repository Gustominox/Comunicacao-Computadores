import logging 
import sys


def logLevel(level):
    levels = {
        1: logging.DEBUG,
        2: logging.INFO,
        3: logging.WARNING,
        4: logging.ERROR,
        5: logging.CRITICAL,
    }

    return levels.get(level,0)    


