#coding:utf8

'''An example of multiprocessing-logger.
Please revise the codes to fit your projcet.
'''

import random
import logging
import multiprocessing as mp
import threading


class QueueHandler(logging.Handler):

    def __init__(self, queue):
        '''init with a process-safe queue'''
        logging.Handler.__init__(self)
        self.queue = queue

    def emit(self, record):
        try:
            self.queue.put_nowait(record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


def config_queue_logger(queue):
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    hdr = QueueHandler(queue)
    root.addHandler(hdr)


def worker(queue, name):
    config_queue_logger(queue)
    logger = logging.getLogger(name)
    levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR,
              logging.CRITICAL]
    for i in xrange(20):
        lvl = random.choice(levels)
        logger.log(lvl, 'Message: %d' % (i,))


def config_file_logger():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    hdlr = logging.FileHandler('test.log')
    fmt = logging.Formatter('[%(name)s][PID:%(process)d][%(asctime)s][%(levelname)s]'
                            '[%(filename)s:%(lineno)s][%(message)s]')
    hdlr.setFormatter(fmt)
    root.addHandler(hdlr)


def log_listener(queue):
    config_file_logger()
    for record in iter(queue.get, None):
        logger = logging.getLogger(record.name)
        logger.handle(record)


def main():
    # mp.log_to_stderr()

    queue = mp.Queue()

    workers = []
    for i in xrange(5):
        p = mp.Process(target=worker, args=(queue, 'proc-%d' % (i,)))
        workers.append(p)
        p.start()

    for p in workers:
        p.join()

    queue.put(None)

    # put the `listener` after other processes
    listener = threading.Thread(target=log_listener, args=(queue,))
    listener.start()
    listener.join()


if __name__ == '__main__':
    main()
