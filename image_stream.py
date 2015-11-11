import os
import urllib.request
import moduls.urls as urls

fourchan_base_url = "https://boards.4chan.org/"
fourchan_cdn_url = "https://i.4cdn.org/"
download_dir = "download"


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
        current_jpg_links = urls.get_jpg_links(boards=['wg',])
        # diff 
        for i, jpg_link in enumerate(current_jpg_links):
            #time.sleep(1)
            download_jpg(jpg_link, str(i)+".jpg")

        #time.sleep(10)


setup()
main()