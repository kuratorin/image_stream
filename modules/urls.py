import re

fourchan_base_url = "https://boards.4chan.org/"
fourchan_cdn_url = "https://i.4cdn.org/"
download_dir = "download"


def get_links_from_html(html, pattern=None, prefix=None):
    if pattern:
        re_links = re.compile(pattern)
        links = list()
        unique_links = list()
        for link in re_links.findall(html):
            if prefix:
                link = prefix + link
            links.append(link)

        for link in set(links):
            unique_links.append(link)

        return unique_links
    else:
        raise Exception()
