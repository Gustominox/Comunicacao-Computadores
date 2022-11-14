import logging as log

DEBUG_MODE = True


def innit_log(LOGFILE):
    log.basicConfig(level=log.DEBUG,
                    format='%(asctime)s:%(levelname)-8s: %(message)s',
                    filename=LOGFILE,
                    filemode='w',
                    datefmt='%d-%m-%y %H:%M:%S')


def debug(msg):
    if DEBUG_MODE:
        print(msg)

    log.debug(msg)


def exception(msg):
    if DEBUG_MODE:
        print(msg)

    log.exception(msg)
