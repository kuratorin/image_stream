import logging
import re
from .abstract import MediaComponent

logger = logging.getLogger('debug')


class Picture(MediaComponent):
    def content(self):
        raise NotImplementedError

    def __init__(self, url):
        super(Picture, self).__init__(url)


class JPG(Picture):
    def __init__(self, url):
        super(JPG, self).__init__(url)

    @property
    def content(self):
        raise NotImplementedError

    @property
    def filename(self):
        logger.info("{}'s filename has been requested".format(self))
        re_filename = re.compile("\d*.jpg")
        filename = re_filename.findall(self.url)[0]

        return filename
