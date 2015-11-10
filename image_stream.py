import urllib.request
import re
import os
import time

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
    re_board_letter = re.compile("/[a-z]/")
    board_letter = re_board_letter.findall(url)[0][1]
    return board_letter

def get_jpg_links(boards=['b',]):
    thread_urls = get_thread_links(boards=boards)
    re_jpg_links = re.compile("\d*.jpg")
    links = list()
    for url in thread_urls:
        board_letter = get_board_letter_from_url(url)
        html = get_html_as_string_from_url(url)
        rel_thread_links = get_links_from_html(html, pattern=re_jpg_links)
        for rel_link in rel_thread_links:
            abs_link = fourchan_cdn_url + board_letter + "/" + rel_link
            links.append(abs_link)
    return links

def setup_download_dir():
    try:
        os.mkdir(download_dir)
    except OSError:
        return

def download_jpg(url, filename):
    print(url, "downloading...")
    try:
        urllib.request.urlretrieve(url, filename)
    except urllib.error.HTTPError:
        print("download error!")
        pass


def setup():
    setup_download_dir()
    return

def main():
    ordered_image_links = list()
    images_downloaded = list()
    images_showen = list()

    while(True):
        current_jpg_links = get_jpg_links(boards=['b',])
        # diff 
        for i, jpg_link in enumerate(current_jpg_links):
            #time.sleep(1)
            download_jpg(jpg_link, str(i)+".jpg")

        #time.sleep(10)


setup()
main()