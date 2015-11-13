import re

fourchan_base_url = "https://boards.4chan.org/"
fourchan_cdn_url = "https://i.4cdn.org/"
download_dir = "download"


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
