import urllib.request


def get_html_as_string_from_url(url):
    http_response = urllib.request.urlopen(url)
    return http_response.read().decode("utf8")


def download_jpg(url, filename=None):
    if not filename:
        filename = url.rpartition("/")[-1]

    try:
        urllib.request.urlretrieve(url, filename)
        # http_response = urllib.request.urlopen(url)
        # check_mime_type(http_response, "image/jpeg")
        # file_name = get_file_name(http_response)
    except urllib.error.HTTPError:
        print("download error!")

    return filename

def get_file_name(http_response):
    print(type(http_response.read()))
    print(http_response.info())


def check_mime_type(url, mime_type):
    pass