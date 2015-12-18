import os
import time
import datetime

while(1):
   dir_to_search = os.path.curdir
   for dirpath, dirnames, filenames in os.walk(dir_to_search):
      if len(filenames) > 100:
         for file in filenames:
            curpath = os.path.join(dirpath, file)
            if curpath.endswith(".jpg"):
               file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(curpath))
               if datetime.datetime.now() - file_modified > datetime.timedelta(minutes=20):
                  os.remove(curpath)
   time.sleep(60)