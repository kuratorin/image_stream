#!/usr/bin/env python3

import re
import urllib.request
import modules.urls

fourchan_base_url = "https://boards.4chan.org/"
fourchan_cdn_url = "https://i.4cdn.org/"


class Component:

    def __init__(self, url):
        self.url = url
        if self.alive:
            self.used = False
        else:
            self.used = True

    def __str__(self):
        return self.url

    @property
    def alive(self):
        http_response = urllib.request.urlopen(self.url)
        if http_response.getcode() == 200:
            return True
        else:
            return False


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
        self.threads = list()
        self.known_thread_links = list()

    @property
    def id(self):
        re_board_letter = re.compile("/[a-z,0-9]{1,3}/")
        board_letter = re_board_letter.findall(self.url)[0]
        board_letter = board_letter.partition("/")[-1].partition("/")[0]

        return board_letter

    def fetch_new_threads(self, max_amount=5):
        re_thread_links = re.compile("thread/\d*")
        new_threads = list()
        board_main_html = self.content
        fetched_rel_links = modules.urls.get_links_from_html(board_main_html, pattern=re_thread_links)

        for rel_link in fetched_rel_links:
            if (len(new_threads) < max_amount):
                abs_link = self.url + rel_link
                if not abs_link in self.known_thread_links:
                    self.known_thread_links.append(abs_link)
                    new_thread = Thread(abs_link)
                    new_threads.append(new_thread)
            else:
                break

        self.threads += new_threads


class MediaComponent(Component):
    def __init__(self, url):
        super(MediaComponent, self).__init__(url)


class Picture(MediaComponent):
    def __init__(self, url):
        super(Picture, self).__init__(url)


class JPG(Picture):
    def __init__(self, url):
        super(JPG, self).__init__(url)