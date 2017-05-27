from __future__ import unicode_literals
from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
from flask import after_this_request

from datetime import datetime
import os

import youtube_dl

class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        print('%s - Done downloading, now converting ...' % datetime.now())

convert_to_mp3 = True
if convert_to_mp3:
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'outtmpl': '%(title)s.%(ext)s',
        'restrictfilenames': True,
    }
else:
    pass
    # todo

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            file_name = ydl.prepare_filename(info_dict)
            ydl.download([url])
        if convert_to_mp3:
            file_name = '%s.mp3' % os.path.splitext(file_name)[0]

        @after_this_request
        def remove_file(response):
            try:
                os.remove(file_name)
            except Exception as error:
                print("Error removing file")
            return response

        return send_file(file_name, as_attachment=True)

    elif request.method == 'GET':
        pass
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80)
