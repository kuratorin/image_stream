#!/usr/bin/env python3

import re
import urllib.request

fourchan_base_url = "https://boards.4chan.org/"
fourchan_cdn_url = "https://i.4cdn.org/"


class Component:

    def __init__(self, url):
        self.url = url
        self.used = False

    @property
    def content_type(self):
        http_response = urllib.request.urlopen(self.url)
        return http_response.info().get("Content-Type")

    @property
    def content(self):
        switcher = {
            'image/jpeg': self.get_jpg,
            'text/html; charset=utf-8': self.get_html,
        }
        # Get the function from switcher dictionary
        func = switcher.get(self.content_type)
        # Execute the function
        return func()

    def get_html(self):
        http_response = urllib.request.urlopen(self.url)
        return http_response.read().decode("utf8")

    def get_jpg(self):
        raise NotImplementedError

    def set_used(self):
        self.used = True


class Thread(Component):
    def __init__(self, url):
        super(Thread, self).__init__(url)


class Board(Component):
    def __init__(self, url):
        super(Board, self).__init__(url)
        self.id = self.get_board_id()
        self.threads = list()

    def get_board_id(self):
        re_board_letter = re.compile("/[a-z,0-9]{1,3}/")
        board_letter = re_board_letter.findall(self.url)[0]
        board_letter = board_letter.partition("/")[-1].partition("/")[0]

        return board_letter

    def get_threads(self, max_amount=5):
        links = list()
        re_thread_links = re.compile("thread/\d*")
        board_main_html = download.get_html_as_string_from_url(self.url)
        rel_links = get_links_from_html(board_main_html, pattern=re_thread_links)
        for rel_link in rel_links:
            abs_link = board_link + rel_link
            links.append(abs_link)
        self.threads = links


class MediaComponent(Component):
    def __init__(self, url):
        super(MediaComponent, self).__init__(url)


class Picture(MediaComponent):
    def __init__(self, url):
        super(Picture, self).__init__(url)


class JPG(Picture):
    def __init__(self, url):
        super(JPG, self).__init__(url)


c = Board("https://boards.4chan.org/b/")

print(c.content_type)
print(c.content)