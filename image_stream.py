import os
import time

import modules.urls as urls
import modules.download as download

fourchan_base_url = "https://boards.4chan.org/"
fourchan_cdn_url = "https://i.4cdn.org/"
download_dir = "download"


def setup_download_dir():
    try:
        os.mkdir(download_dir)
    except OSError:
        return

def setup():
    setup_download_dir()
    return

def main():
    ordered_image_links = list()
    images_to_downloaded = list()
    images_downloaded = list()
    images_showen = list()

    current_jpg_links = set()
    known_jpg_links = set()
    new_jpg_links = list()

    while(True):
        current_jpg_links = urls.get_jpg_links(boards=['fa',''])
        new_jpg_links = current_jpg_links.difference(set(known_jpg_links))
        print("{} new jpg links found".format(len(new_jpg_links)))

        for i, jpg_link in enumerate(new_jpg_links):
            print("[{} / {} / {}] {} downloading...".format(
                str(len(known_jpg_links)).zfill(4),
                str(i).zfill(4),
                str(len(new_jpg_links)).zfill(4),
                jpg_link))
            jpg = download.download_jpg(jpg_link)
            if jpg:
                known_jpg_links.add(jpg_link)

        print("Picture batch downloaded!!!!!!!!")
        print("Picture batch downloaded!!!!!!!!")
        print("Picture batch downloaded!!!!!!!!")
        print("Picture batch downloaded!!!!!!!!")
        print("Picture batch downloaded!!!!!!!!")

        time.sleep(5)


setup()
main()