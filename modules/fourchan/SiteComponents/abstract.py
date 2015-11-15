#!/usr/bin/env python3

import logging
import re
import requests
import requests.exceptions

fourchan_base_url = "https://boards.4chan.org/"
fourchan_cdn_url = "https://i.4cdn.org/"

logger = logging.getLogger('debug')


class Component:
    def __init__(self, url):
        self.url = url
        # requests.Response()
        self.downloaded = False
        self.downloaded_http_response = None
        self.marked_as_can_be_deleted = False

    def __str__(self):
        return self.url

    @property
    def http_response(self, force_update=False):
        logger.debug("{}'s http_response has been requested".format(self))
        if force_update or not self.downloaded_http_response:
            try:
                self.downloaded_http_response = requests.get(self.url, timeout=2.0)
                logger.debug("{}'s http_response was downloaded".format(self))
                return self.downloaded_http_response
            except requests.exceptions.RequestException:
                logger.error("error while http request".format(self))
                return None
        else:
            logger.debug("{}'s cached http_response was returned".format(self))
            return self.downloaded_http_response

    @property
    def is_alive(self):
        logger.debug("{}'s is_alive status has been requested".format(self))
        if self.http_response is None:
            return False
        else:
            return True

    @property
    def http_code(self):
        if self.is_alive:
            return self.http_response.status_code
        else:
            return "404"

    @property
    def content_type(self):
        logger.debug("{}'s http_response has been requested".format(self))
        if self.is_alive:
            return self.http_response.headers["Content-Type"]
        else:
            return None

    # abstract
    @property
    def content(self):
        raise NotImplementedError

    @property
    def board_id(self):
        logger.debug("{}'s board_id has been requested".format(self))
        re_board_letter = re.compile("/[a-z,0-9]{1,3}/")
        board_letter = re_board_letter.findall(self.url)[0]
        board_letter = board_letter.partition("/")[-1].partition("/")[0]

        return board_letter

    def set_used(self):
        self.marked_as_can_be_deleted = True
        logger.debug("{}'s marked_as_can_be_deleted has been set".format(self))


class HTMLComponent(Component):
    def __init__(self, url):
        super(HTMLComponent, self).__init__(url)
        logger.debug("{} is instantiated".format(self))

    @property
    def content(self):
        logger.info("{}'s content has been requested".format(self))
        if self.is_alive:
            return self.http_response.text
        else:
            return None


class MediaComponent(Component):
    def __init__(self, url):
        super(MediaComponent, self).__init__(url)
        logger.info("{} is instantiated".format(self))
        self.media_byte_data = bytes()

    @property
    def content(self):
        logger.info("{}'s board_id has been requested".format(self))
        if not self.downloaded:
            self.download()
        return self.media_byte_data

    @property
    def filename(self):
        raise NotImplementedError

    def download(self):
        logger.info("{}'s will be downloaded".format(self))
        try:
            r = self.http_response
            if r.status_code == 200:
                with open(self.filename, 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
                self.downloaded = True
        except requests.exceptions.RequestException:
            logger.error("download failed...")
            self.marked_as_can_be_deleted = True
