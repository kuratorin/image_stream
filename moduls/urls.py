import re
import urllib

fourchan_base_url = "https://boards.4chan.org/"
fourchan_cdn_url = "https://i.4cdn.org/"
download_dir = "download"

def get_html_as_string_from_url(url):
    http_response = urllib.request.urlopen(url)
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

def get_board_letter_from_url(url):
    re_board_letter = re.compile("/[a-z,0-9]{1,3}/")
    board_letter = re_board_letter.findall(url)[0]
    board_letter = board_letter.partition("/")[-1].partition("/")[0]

    return board_letter


def get_jpg_links(boards=['b',]):
    """

    :type boards: list(str)
    """
    thread_urls = get_thread_links(boards=boards)
    re_jpg_links = re.compile("\d{4,16}.jpg")
    links = list()
    for url in thread_urls:
        board_letter = get_board_letter_from_url(url)
        html = get_html_as_string_from_url(url)
        rel_thread_links = get_links_from_html(html, pattern=re_jpg_links)
        for rel_link in rel_thread_links:
            abs_link = fourchan_cdn_url + board_letter + "/" + rel_link
            links.append(abs_link)
    return links