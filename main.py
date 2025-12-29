import sys
import yt_dlp
import os
import flask

app = flask.Flask(__name__)

def clean_string(text):
    s = ''.join(char for char in text if char.isalnum() or char in '-_ ')
    return ' '.join(s.split())

def download(url):
    index = 1
    workdir = os.path.join(os.getcwd(), 'out')
    tmpdir = os.path.join(os.getcwd(), 'tmp')

    opts = {
        'js_runtimes': {
            'node': {}
        },
        'remote_components': ['ejs:github'],
    }

    with yt_dlp.YoutubeDL(opts) as dl:
        info = dl.sanitize_info(dl.extract_info(url, download=False))
        channel = info.get('uploader_id')
        title = info.get('title')

        channel = clean_string(channel)
        title = clean_string(title)

    if os.path.exists(os.path.join(workdir, channel, f'#{index:03d} - {title}.mp3')):
        return

    if os.path.exists(os.path.join(workdir, channel)):
        for f in os.listdir(os.path.join(workdir, channel)):
            n = f.split(' ')[0].split('#')[-1]
            int_n = int(n)
            if int_n+1 > index:
                index = int_n+1

    opts = {
        'format': 'ba[acodec^=mp3]/ba/b',
        'outtmpl': f'out/{channel}/#{index:03d} - {title}.%(ext)s',
        # 'writethumbnail': True,
        'js_runtimes': {
            'node': {}
        },
        'remote_components': ['ejs:github'],
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': "64",
            },
            # {
            #     'key': 'EmbedThumbnail',
            #     'already_have_thumbnail': False,
            # },
            # {
            #     'key': 'FFmpegMetadata',
            #     'add_metadata': True,
            # }
        ]
    }
    

    with yt_dlp.YoutubeDL(opts) as dl:
        err = dl.download(url)

@app.route('/')
def root_handler():
    if flask.request.method == 'POST':
        data = flask.request.get_data()
        print(data)
    return 'ok'

if __name__ == "__main__":
    # download(sys.argv[1])
    app.run(host="0.0.0.0", port=9000)

