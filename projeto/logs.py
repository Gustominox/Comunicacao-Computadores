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

# logging.basicConfig(level=logLevel(1),
#                     format='%(asctime)s %(levelname)8s \t%(message)s',
#                     filename='./myapp.log',
#                     filemode='w',
#                     datefmt='%d-%m-%y %H:%M:%S')


# argv = sys.argv[1:]

# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical message')

# print(logLevel(int(argv[0])))