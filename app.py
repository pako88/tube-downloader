from __future__ import unicode_literals
from flask import Flask
from flask import render_template
from flask import request
from flask import send_file

import youtube_dl

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

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
}

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            ydl.download([url])
        file_name = '%s.mp3' % info_dict['title']
        return send_file(file_name, as_attachment=True)
    elif request.method == 'GET':
        pass
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80)
