#!/usr/bin/env python
from __future__ import unicode_literals

import file_queue
import os
import web
import string
from time import sleep
from threading import Thread
from youtube_dl import YoutubeDL
from youtube_dl.utils import sanitize_path, compat_str

q = file_queue.FileQueue('videos_to_dl')

allowed_chars = unicode(string.ascii_letters+string.digits+"!@#$%^&*()_+\|{}[]-_=+'\",.<>?:; ")

class MyYoutubeDL(YoutubeDL):
    def prepare_filename(self, info_dict):
        filename = sanitize_path(info_dict["title"])
        filename = filename.replace(u'\u3010', u'[').replace(u'\u3011', u']')
        for char in filename[:]:
            if char not in allowed_chars:
                filename = filename.replace(char, u'')
        return compat_str(filename)

opts = {
"postprocessors":[{"key":'FFmpegExtractAudio', "preferredcodec":"mp3", "preferredquality":"0"}]
}

music_dir = "/media/16GB-Music/Music"

class Favicon():
    def GET(self):
        return web.seeother('static/favicon.ico')

class MainPage():
    def GET(self):
        if 'v' in web.input():
            link = "http://youtube.com/watch?v={}".format(web.input()['v'])
            q.put(link)
            print(link)
            return web.seeother(link)
        else:
            return "Whoosh"
        
    def POST(self):
        return "Woot woot"



def dl_thread():
    while True:
        link = q.get()
        if link is not None:
            download(link)
        else:
            sleep(1)

def download(link):
    with MyYoutubeDL(opts) as ydl:
        ydl.download([link])

urls = ("/favicon.ico", "Favicon",
"/.*", "MainPage")
app = web.application(urls, globals())
web.debug = False

if __name__ == "__main__":
    os.chdir(music_dir)
    t = Thread(target=dl_thread)
    t.daemon = True
    t.start()
    app.run()
