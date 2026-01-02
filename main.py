import sys
import yt_dlp
import os
import json
import argparse
import queue
import signal
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

Q = queue.Queue()
shutdown_event = threading.Event()


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        try:
            data_obj = json.loads(body)

            event_type = data_obj['event_type']
            if event_type != 'save_entry':
                raise Exception('Bad event type')

            url = data_obj['entry']['url']
        except Exception as e:
            print(e)
            print(f'bad event')
        else:
            Q.put(url)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'ok')


server = HTTPServer(("0.0.0.0", 9000), Handler)

def sigint_handler(sig, frame):
    print('CTRL + C occured')
    shutdown_event.set()
    Q.shutdown()
    server.shutdown()
    server.server_close()



def clean_string(text):
    s = ''.join(char for char in text if char.isalnum() or char in '-_ ')
    return ' '.join(s.split())


def download(url, music=False):
    index = 1
    workdir = os.getenv('WORKDIR', os.path.join(os.getcwd(), 'out'))

    opts = {
        'js_runtimes': {
            'deno': {}
        },
        'remote_components': ['ejs:github'],
    }

    with yt_dlp.YoutubeDL(opts) as dl:
        try:
            info = dl.sanitize_info(dl.extract_info(url, download=False))
        except:
            print(f'ERROR: bad url: {url}')
            return False

        channel_original = info.get('uploader_id')
        title_original = info.get('title')

        channel = clean_string(channel_original)
        title = clean_string(title_original)


    if not music and os.path.exists(os.path.join(workdir, channel)):
        for f in os.listdir(os.path.join(workdir, channel)):
            n = f.split(' ')[0].split('#')[-1]
            int_n = int(n)
            if int_n+1 > index:
                index = int_n+1

        for f in os.listdir(os.path.join(workdir, channel)):
            if f.endswith(f' - {title}.mp3'):
                print(f'EXISTS: {url}')
                print(f'EXISTS: {f}')
                return

    opts = {
        'format': 'ba[acodec^=mp3]/ba/b',
        'outtmpl': f'{workdir}/{channel}/#{index:03d} - {title}.%(ext)s',
        'writethumbnail': True,
        'js_runtimes': {
            'deno': {}
        },
        'remote_components': ['ejs:github'],
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': "64",
            },
            {
                'key': 'EmbedThumbnail',
                'already_have_thumbnail': False,
            },
            {
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            }
        ]
    }

    if music:
        del(opts['postprocessors'][0]['preferredquality'])
        opts['outtmpl'] = f'{workdir}/{title}.%(ext)s'
        opts['postprocessor_args'] = [
            '-metadata', 'artist=YouTube',
        ]
    

    with yt_dlp.YoutubeDL(opts) as dl:
        err = dl.download(url)


def submitter_thread():
    while not shutdown_event.is_set():
        try:
            url = Q.get(block=True)
        except queue.ShutDown:
            pass
        else:
            print(f'SUBMITTER got url :: {url}')
            download(url)

def downloader_thread():
    pass


def server_thread():
    server.serve_forever()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('url', nargs="*")
    ap.add_argument('--srv', action="store_true", default=False)
    ap.add_argument('--music', action="store_true", default=False)
    args = ap.parse_args()

    if args.srv:
        signal.signal(signal.SIGTERM, sigint_handler)
        signal.signal(signal.SIGINT, sigint_handler)

        _submitter = threading.Thread(target=submitter_thread)
        _server = threading.Thread(target=server_thread)

        _submitter.start()
        _server.start()
        
        _submitter.join()
        _server.join()

        print('ALL CLEAR')
        sys.exit(0)

    for url in args.url:
        download(url, music=args.music)

