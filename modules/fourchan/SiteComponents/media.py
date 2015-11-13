from .abstract import MediaComponent


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
