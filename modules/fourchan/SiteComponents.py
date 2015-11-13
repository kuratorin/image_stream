#!/usr/bin/env python3

import re
import urllib.request
import urllib.error
import modules.urls

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


class HTTPComponent(Component):
    def __init__(self, url):
        super(HTTPComponent, self).__init__(url)

    @property
    def content(self):
        http_response = urllib.request.urlopen(self.url)
        return http_response.read().decode("utf8")


class Board(HTTPComponent):
    def __init__(self, url):
        super(Board, self).__init__(url)
        self.threads = []
        self.known_thread_links = list()

    @property
    def number_of_threads(self):
        return len(self.threads)

    @property
    def thread_links(self):
        re_thread_links = re.compile("https://*thread/\d*")
        html = self.content
        return modules.urls.get_links_from_html(html, pattern=re_thread_links)


    def pop_thread(self):
        return self.threads[0]

    def clean_threads_list(self):
        for thread in self.threads:
            if not thread.is_alive or thread.marked_as_can_be_deleted:
                del thread

    def prepare(self):
        self.clean_threads_list()
        while len(self.threads) < 2:
            self.fetch_new_threads(n=1)
        self.prepare_threads(n=2)

    def prepare_threads(self, n=None):
        """

        :type n: int
        """
        if not n:
            n = self.number_of_threads
        for thread in self.threads[0:n]:
            if not thread.prepared:
                thread.prepare()

    def fetch_new_threads(self, n=1):
        new_threads = []
        for link in self.thread_links:
            if len(new_threads) < n:
                if link not in self.known_thread_links:
                    self.known_thread_links.append(link)
                    new_thread = Thread(link)
                    new_threads.append(new_thread)
            else:
                break

        self.threads += new_threads


class Thread(HTTPComponent):
    def __init__(self, url):
        super(Thread, self).__init__(url)
        self.jpgs = []
        self.known_jpg_links = set()
        self.prepared = False

    @property
    def jpg_links(self):
        re_jpg_links = re.compile("https://*\d{4,16}.jpg")
        html = self.content
        return modules.urls.get_links_from_html(html, pattern=re_jpg_links)

    def prepare(self):
        self.fetch_new_jpgs()
        for jpg in self.jpgs:
            jpg.download()
        self.prepared = True

    def fetch_new_jpgs(self):
        for link in self.jpg_links:
            if link not in self.known_jpg_links:
                new_jpg = JPG(link)
                self.jpgs.append(new_jpg)
            self.known_jpg_links.update(link)

    def pop_jpg(self):
        # view needs to call .set_used() on jpg
        for jpg in self.jpgs:
            if not jpg.marked_as_can_be_deleted:
                return jpg


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


class Picture(MediaComponent):
    def content(self):
        raise NotImplementedError

    def __init__(self, url):
        super(Picture, self).__init__(url)


class JPG(Picture):
    def content(self):
        raise NotImplementedError

    def __init__(self, url):
        super(JPG, self).__init__(url)
