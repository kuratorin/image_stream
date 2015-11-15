import logging
import re
import modules.urls
from .abstract import HTMLComponent
from .media import JPG

logger = logging.getLogger('debug')

class Board(HTMLComponent):
    def __init__(self, url):
        super(Board, self).__init__(url)
        self.threads = []
        self.known_thread_links = list()

    @property
    def number_of_threads(self):
        return len(self.threads)

    @property
    def thread_links(self):
        prefix = "https://boards.4chan.org/" + self.board_id + "/"
        re_string = "thread/\d*"
        re_thread_links = re.compile(re_string)
        html = self.content
        return modules.urls.get_links_from_html(html, pattern=re_thread_links, prefix=prefix)

    def pop_thread(self):
        if len(self.threads) == 0:
            self.fetch_new_threads(n=1)
            self.prepare_threads(n=1)

        thread = self.threads[0]
        self.threads = self.threads[1:-1]
        return thread

    def clean_threads_list(self):
        for thread in self.threads:
            if not thread.is_alive or thread.marked_as_can_be_deleted:
                del thread

    def prepare(self):
        self.clean_threads_list()
        while len(self.threads) < 2:
            self.fetch_new_threads(n=2)
        self.prepare_threads(n=2)

    def prepare_threads(self, n=None):
        """

        :type n: int
        """
        if not n:
            n = self.number_of_threads
        for thread in self.threads[0:n-1]:
            if not thread.prepared:
                thread.prepare()

    def fetch_new_threads(self, n=1):
        new_threads = []
        thread_links = self.thread_links
        for link in thread_links:
            if len(new_threads) < n:
                if link not in self.known_thread_links:
                    self.known_thread_links.append(link)
                    new_thread = Thread(link)
                    new_threads.append(new_thread)
            else:
                break

        self.threads += new_threads


class Thread(HTMLComponent):
    def __init__(self, url):
        super(Thread, self).__init__(url)
        # list of JPG objects
        self.jpgs = []
        self.known_jpg_links = set()
        self.prepared = False

    @property
    def jpg_links(self):
        prefix = "https:"
        re_jpg_links = re.compile("//i.4cdn.org/[a-z,0-9]{1,3}/\d*\.jpg")
        html = self.content
        return modules.urls.get_links_from_html(html, pattern=re_jpg_links, prefix=prefix)

    def prepare(self):
        self.fetch_new_jpgs()
        for jpg in self.jpgs:
            jpg.download()
        self.prepared = True

    def fetch_new_jpgs(self):
        jpg_links = self.jpg_links
        for i, link in enumerate(jpg_links):
            logger.info("{} fetching jpg {} of {}".format(
                self.url,
                str(i+1).zfill(3),
                str(len(jpg_links)).zfill(3)))
            if link not in self.known_jpg_links:
                new_jpg = JPG(link)
                self.jpgs.append(new_jpg)
            self.known_jpg_links.update(link)

    def pop_jpg(self):
        # view needs to call .set_used() on jpg
        for i in range(0, len(self.jpgs)):
            if not self.jpgs[i].marked_as_can_be_deleted:
                jpg = self.jpgs[i]
                self.jpgs[i].set_used()
                return jpg
