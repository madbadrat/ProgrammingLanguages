# url = 'http://marigostra.ru/persist/cbow.txt'
# url = 'https://musify.club/track/dl/3113465/dream-theater-octavarium.mp3'

import argparse
import os
import signal
import threading
import time

import requests

downloaded = 0
completed = threading.Event()
stoped = threading.Event()

def download_file(url):
    response = requests.get(url, stream=True)
    filename = os.path.basename(url)
    global downloaded

    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=4096):
            if chunk and not stoped.is_set():
                file.write(chunk)
                downloaded += len(chunk)

    print('\nDone')
    completed.set()

def timer():
    while not completed.is_set() and not stoped.is_set():
        print('\rDownloaded', downloaded, 'bytes', end='')
        time.sleep(1)

def signal_handler(signal, frame):
    print('\nStopping')
    stoped.set()

signal.signal(signal.SIGINT, signal_handler)

parser = argparse.ArgumentParser()
parser.add_argument('url')
args = parser.parse_args()

downloading_thread = threading.Thread(target=download_file, args=(args.url,))
timer_thread = threading.Thread(target=timer)

downloading_thread.start()
timer_thread.start()

downloading_thread.join()
timer_thread.join()