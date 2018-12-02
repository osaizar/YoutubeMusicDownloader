#!/usr/bin/python

# Author: @osaizar
# Dependencies: pafy, BeautifulSoup, pydub, youtube-dl (just pip install them)
# zip (apt install zip) only for ziping the dir, the program can work with out.

import pafy
import os
import urllib
import optparse
import requests
from bs4 import BeautifulSoup
from pydub import AudioSegment

FILE = "music_file.txt"
OUTPUT_DIR = "music/"
TMP_DIR = "/tmp/"
RAR = False


songs = []

class Song:
    def __init__(self, title, author=None):
        self.title = title
        self.author = author

    def toStr(self):
        rt = self.title
        if self.author != None:
            rt += " - "+self.author

        return rt

def parse_file():
    file = open(FILE, "r")
    author = ""
    for line in file.readlines():
        if line[0] != "#": # it's a comment!
            line = line.replace("\n", "")
            if "::" in line:
                author = line.split("::")[0]
            elif "\n" != line and "" != line:
                if author != "?":
                    songs.append(Song(line, author))
                else:
                    songs.append(Song(line))

def make_dirs():
    for song in songs:
        if song.author != None:
            if not os.path.exists(OUTPUT_DIR+song.author):
                os.makedirs(OUTPUT_DIR+song.author)

def get_link(song):
    query = urllib.quote(song.toStr())
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html,"lxml")
    video = soup.findAll(attrs={'class':'yt-uix-tile-link'})[0]
    return 'https://www.youtube.com' + video['href']

def get_audio(url):
    video = pafy.new(url)
    return video.getbestaudio()

def download_mp3(audio, song):
    lucky_header = {'Range': 'bytes=0-'}
    fast_resp = requests.get(audio.url, headers=lucky_header)
    with open(TMP_DIR+song.title+'.webm', 'wb') as fout:
        fout.write(fast_resp.content)

def convert_2_mp3(song):
    if song.author == None:
        path = song.title+".mp3"
    else:
        path = song.author+"/"+song.title+".mp3"

    AudioSegment.from_file(TMP_DIR+song.title+'.webm').export(OUTPUT_DIR+path, format="mp3")
    os.remove(TMP_DIR+song.title+'.webm')

def zip_dir():
    print "ziping directory..."
    os.system("zip "+OUTPUT_DIR[:-1]+".zip "+OUTPUT_DIR[:-1]+" -rm")
    print "complete!  \n"

def parse_args():
    parser = optparse.OptionParser('Usage [-f <Music file>][-z][-s]')

    parser.add_option('-f', dest='file', type='string', \
                        help='music file')
    parser.add_option('-z', dest='rar', action="store_true", \
                        help='Makes a zip file for the output')

    (options, args) = parser.parse_args()

    file = options.file
    rar = options.rar

    if file == None:
        file = FILE
    if rar == None:
        rar = RAR

    return rar, file


def main():
    RAR, FILE = parse_args()

    parse_file()
    make_dirs()
    song_n = len(songs)

    for i, song in enumerate(songs):
        print str(i)+"/"+str(song_n)+" ["+str((i*100)/song_n)+"%] "+song.toStr()
        url = get_link(song)
        audio = get_audio(url)
        download_mp3(audio, song)
        convert_2_mp3(song)

    if RAR:
        zip_dir()

if __name__ == '__main__':
    main()
