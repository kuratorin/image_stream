from urllib.request import urlopen
import re

fourchan_base_url = "https://boards.4chan.org/"

def get_html_as_string_from_url(url):
    http_response = urlopen(url)
    return http_response.read().decode("utf8")

def get_links_from_html(html, pattern=None):
    if re:
        re_rel_thread_links = re.compile(pattern)
        rel_thread_links = list()
        unique_rel_thread_links = list()

        for rel_thread_link in re_rel_thread_links.findall(html):
            rel_thread_links.append(rel_thread_link)

        for unique_rel_thread_link in set(rel_thread_links):
            unique_rel_thread_links.append(unique_rel_thread_link)

        return unique_rel_thread_links
    else:
        raise Exception()

def get_thread_links(boards=['b',]):
    re_thread_links = re.compile("thread/\d*")
    links = list()
    for board in boards:
        board_link = fourchan_base_url + board + "/"
        board_main_html = get_html_as_string_from_url(board_link)
        rel_links = get_links_from_html(board_main_html, pattern=re_thread_links)
        for rel_link in rel_links:
            abs_link = board_link + rel_link
            links.append(abs_link)
    return links


thread_links = get_thread_links(boards=['a', 'b', 'c'])

for i in thread_links:
    print(i)


