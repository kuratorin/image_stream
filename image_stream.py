import logging
import os
import modules.fourchan as fourchan
import modules.fourchan.SiteComponents as SiteComponents


# create logger with 'spam_application'
logger = logging.getLogger('debug')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
# fh = logging.FileHandler('spam.log')
# fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
# logger.addHandler(fh)
logger.addHandler(ch)

download_dir = "download"

def setup_download_dir():
    try:
        os.mkdir(download_dir)
    except OSError:
        return


def setup():
    setup_download_dir()
    return


def main():
    boards = list()
    for board_id in fourchan.BOARDS:
        board_url = fourchan.SITE_URL + board_id + "/"
        board = SiteComponents.Board(board_url)
        boards.append(board)

    while(True):
        for board in boards:
            logger.info("---------- preparing board ----------")
            board.prepare()
            logger.info("---------- board prepared ----------")
            i = 0
            for i in range(0, 2):
                thread = board.pop_thread()
                logger.info("---------- preparig thread ----------")
                thread.prepare()
                logger.info("---------- thread prepared ----------")
                i += i
                jpg = thread.pop_jpg()
                while jpg:
                    logger.info("popping jpg {}".format(jpg))
                    jpg = thread.pop_jpg()
                    # gui.display(jpg)

setup()
main()
