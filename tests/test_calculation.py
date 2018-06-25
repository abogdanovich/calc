""" Configuration file for 'Pytest'.
    Main tests for calculator

"""

import logging
from os import path
from time import strftime

################################################
# Logging
################################################


LOGGING_LEVEL = 'INFO'
INDENT = '==================================================='
TIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

# Unique log file name
LOG_DIR = './'
LOG_PATH = path.join(LOG_DIR, 'calc_{}.log'.format(strftime(TIME_FORMAT)))

# Init logger for common messages
logger = logging.getLogger('Common')

if LOGGING_LEVEL.upper() == 'DEBUG':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# Add console handler to logger

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
logger.addHandler(stream_handler)

# Add file handler to logger
file_handler = logging.FileHandler(LOG_PATH)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
logger.addHandler(file_handler)