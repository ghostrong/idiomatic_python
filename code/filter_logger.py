#coding:utf8

'''A logger containning two handlers:
Write the messages of level `DEBUG` and `INFO` to one file,
while write the messages of higher levels to another file.
i.e., handling records with different handlers according their
levels.
'''

import random
import logging

# config for the `root` handler
# it will ignore every record
logging.getLogger().addHandler(logging.NullHandler())

class LevelFilter(logging.Filter):
    '''a filter which only accept records whose levels are
    with the range defined by `min_level` and `max_level`
    '''

    def __init__(self, min_level, max_level):
        self.min_level = min_level
        self.max_level = max_level

    def filter(self, record):
        return (record.levelno >= self.min_level and
                record.levelno <= self.max_level)


def get_logger():
    fmt = logging.Formatter('[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d]'
                            '[%(message)s]')

    # a handler for (DEBUG, INFO)
    hdlr = logging.FileHandler('simple_logger.log')
    hdlr.setFormatter(fmt)
    hdlr.addFilter(LevelFilter(logging.DEBUG, logging.INFO))

    # a handler for (WARNING, ERROR, CRITICAL)
    hdlr_wf = logging.FileHandler('simple_logger.log.wf')
    hdlr_wf.setFormatter(fmt)
    hdlr_wf.addFilter(LevelFilter(logging.WARNING, logging.CRITICAL))

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(hdlr)
    logger.addHandler(hdlr_wf)

    return logger


def main():
    logger = get_logger()
    levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR,
              logging.CRITICAL]

    for i in xrange(100):
        lvl = random.choice(levels)
        logger.log(lvl, 'Message: %d' % (i,))


if __name__ == '__main__':
    main()
