#!/usr/bin/env python3

import re
import urllib.request
import urllib.error

fourchan_base_url = "https://boards.4chan.org/"
fourchan_cdn_url = "https://i.4cdn.org/"


class Component:
    def __init__(self, url):
        self.url = url
        if self.is_alive:
            self.marked_as_can_be_deleted = False
        else:
            self.marked_as_can_be_deleted = True

    def __str__(self):
        return self.url

    @property
    def http_response(self):
        try:
            return urllib.request.urlopen(self.url)
        except urllib.error.HTTPError:
            return None

    @property
    def is_alive(self):
        if self.http_response is None:
            return False
        else:
            return True

    @property
    def http_code(self):
        if self.is_alive:
            return self.http_response.getcode()

    @property
    def content_type(self):
        return self.http_response.info().get("Content-Type")

    # abstract
    @property
    def content(self):
        raise NotImplementedError

    @property
    def board_id(self):
        re_board_letter = re.compile("/[a-z,0-9]{1,3}/")
        board_letter = re_board_letter.findall(self.url)[0]
        board_letter = board_letter.partition("/")[-1].partition("/")[0]

        return board_letter

    def set_used(self):
        self.marked_as_can_be_deleted = True


class HTMLComponent(Component):
    def __init__(self, url):
        super(HTMLComponent, self).__init__(url)

    @property
    def content(self):
        http_response = urllib.request.urlopen(self.url)
        return http_response.read().decode("utf8")


class MediaComponent(Component):
    def __init__(self, url):
        super(MediaComponent, self).__init__(url)
        self.downloaded = False
        self.downloaded_data = bytes()

    @property
    def content(self):
        if not self.downloaded:
            self.download()
        return self.downloaded_data

    def download(self):
        if self.is_alive:
            filename = self.url.rpartition("/")[-1]
            print("{} downloading...".format(self.url))
            http_response = urllib.request.urlopen(self.url)
            print(http_response.read())
            # urllib.request.urlretrieve(self.url, filename)
            self.downloaded = True
        else:
            self.marked_as_can_be_deleted = True
