#coding:utf8

import logging

class OneLineFormatter(logging.Formatter):

    def formatException(self, exc_info):
        s = super(self.__class__, self).formatException(exc_info)
        return '[EXCEPTION: %s]' % (repr(s),)

    def format(self, record):
        s = super(self.__class__, self).format(record)
        return s.replace('\n', ' ')


def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # fmt = logging.Formatter('[%(levelname)s][%(asctime)s][%(message)s]')
    fmt = OneLineFormatter('[%(levelname)s][%(asctime)s][%(message)s]')
    hdlr = logging.FileHandler('exception.log')
    hdlr.setFormatter(fmt)
    logger.addHandler(hdlr)
    return logger


def main():
    logger = get_logger()
    try:
        print a
    except NameError as e:
        logger.exception(e)


if __name__ == '__main__':
    main()
