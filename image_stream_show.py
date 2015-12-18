import logging
import time
import os
import modules.fourchan as fourchan
import modules.fourchan.SiteComponents as SiteComponents
import tkinter
from PIL import ImageTk, Image

# create logger with 'spam_application'
logger = logging.getLogger('info')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
# fh = logging.FileHandler('spam.log')
# fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
# logger.addHandler(fh)
logger.addHandler(ch)

download_dir = "download"

class App():
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.configure(background='black')
        image1=Image.open('test.jpg')
        self.root.geometry("{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.tkpi=ImageTk.PhotoImage(image1)
        label_image=tkinter.Label(self.root, image=self.tkpi)
        label_image.place(x=self.root.winfo_screenwidth()/2,y=self.root.winfo_screenwidth()/2,width=image1.size[0],height=image1.size[1])

        self.displayed_images = []
        self.update_image()
        self.hide_image()
        self.root.mainloop()


    def update_image(self):
        current_image=Image.open(self.get_image_path())
        self.tkpi=ImageTk.PhotoImage(current_image)
        label_image=tkinter.Label(self.root, image=self.tkpi)
        label_image.configure(background='black')
        label_image.place(relx=0.5,rely=0.5,anchor='center')

        print("slide")
        self.root.after(2000, self.update_image)

    def hide_image(self):
        current_image=Image.open("black.jpg")
        self.tkpi=ImageTk.PhotoImage(current_image)
        label_image=tkinter.Label(self.root, image=self.tkpi)
        label_image.configure(background='black')
        label_image.place(relx=0.5,rely=0.5,anchor='center')

        print("hidden")
        self.root.after(2000, self.hide_image)

    def get_image_path(self):
        if len(self.displayed_images) > 100:
            logger.info("len(self.displayed_images) = {}".format(len(self.displayed_images)))
            self.displayed_images = self.displayed_images[9:-1]
            logger.info("len(self.displayed_images) = {}".format(len(self.displayed_images)))
        for file_path in set(os.listdir("./")):
            if file_path.endswith(".jpg"):
                if file_path not in self.displayed_images:
                    self.displayed_images.append(file_path)
                    return file_path


def setup_download_dir():
    try:
        os.mkdir(download_dir)
    except OSError:
        return


def setup():

    return


def main():
    boards = list()
    for board_id in fourchan.BOARDS:
        board_url = fourchan.SITE_URL + board_id + "/"
        board = SiteComponents.Board(board_url)
        boards.append(board)

    while(True):
        for board in boards:
            logger.info("---------- preparing board ----------")
            board.prepare()
            logger.info("---------- board prepared ----------")
            i = 0
            for i in range(0, 2):
                thread = board.pop_thread()
                logger.info("---------- preparig thread ----------")
                thread.prepare()
                logger.info("---------- thread prepared ----------")
                i += i
                jpg = thread.pop_jpg()
                while jpg:
                    logger.info("popping jpg {}".format(jpg))
                    jpg = thread.pop_jpg()
                    time.sleep(0.2)
                    # gui.display(jpg)

app = App()
setup()
main()
