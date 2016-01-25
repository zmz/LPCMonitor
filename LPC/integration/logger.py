__author__ = 'zhangxg'

import logging

from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
import time

def create_rotating_log(path):
    """
    Creates a rotating log
    """
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)

    # add a rotating handler
    handler = RotatingFileHandler(path, maxBytes=20,
                                  backupCount=2)
    logger.addHandler(handler)

    for i in range(10):
        logger.info("This is test log line %s" % i)
        time.sleep(1.5)


def create_timed_rotating_log(path):
    """"""
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)

    handler = TimedRotatingFileHandler(path,
                                       # filemode='a',
                                       when="MIDNIGHT",
                                       format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                                       # datefmt='%H:%M:%S',
                                       interval=1,
                                       backupCount=5)
    logger.addHandler(handler)

    for i in range(6):
        logger.info("This is a test!")
        time.sleep(10)


if __name__ == "__main__":
    log_file = "/home/zhangxg/work/timed_test.log"
    create_timed_rotating_log(log_file)
    # create_timed_rotating_log(log_file)

# logging.basicConfig(filename='/home/zhangxg/work/test.log',
#                             filemode='a',
#                             format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                             datefmt='%H:%M:%S',
#                             level=logging.ERROR)
#
# logging.info("Running Urban Planning")
#
#
# logging.info("Running Urban bbbbbbbbbbbb")
#
#
# logging.error('this is an error message')
# self.logger = logging.getLogger('urbanGUI')