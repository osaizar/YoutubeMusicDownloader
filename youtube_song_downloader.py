#!/usr/bin/python

# Author: @osaizar
# Dependencies: pafy, BeautifulSoup, pydub, youtube-dl (just pip install them)
# zip (apt install zip) only for ziping the dir, the program can work with out.

import pafy
import os
import urllib
import urllib2
import optparse
from bs4 import BeautifulSoup
from pydub import AudioSegment

FILE = "music_file.txt"
OUTPUT_DIR = "music/"
RAR = False

songs = []

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
                    songs.append(author+" - "+line)
                else:
                    songs.append(line)

def make_dirs():
    for song in songs:
        song_data = song.split(" - ")
        if len(song_data) > 1 and not os.path.exists(OUTPUT_DIR+song_data[0]):
            os.makedirs(OUTPUT_DIR+song_data[0])

def get_link(song):
    query = urllib.quote(song)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html,"lxml")
    video = soup.findAll(attrs={'class':'yt-uix-tile-link'})[0]
    return 'https://www.youtube.com' + video['href']

def get_audio(url):
    print "checking URL..."
    video = pafy.new(url)
    print "Got "+video.title
    return video.getbestaudio()

def download_mp3(audio, song):
    song_data = song.split(" - ")
    raw_audio_title = audio.title+"."+audio.extension
    if len(song_data) > 1:
        mp3_audio_title = song_data[0]+"/"+song_data[1]+".mp3"
    else:
        mp3_audio_title = song_data[0]+".mp3"

    print "Starting download..."
    audio.download()
    print "\nConverting to mp3..."
    AudioSegment.from_file(raw_audio_title).export(OUTPUT_DIR+mp3_audio_title, format="mp3")
    os.remove(raw_audio_title)
    print "Done! \n"

def zip_dir():
    print "ziping directory..."
    os.system("zip "+OUTPUT_DIR[:-1]+".zip "+OUTPUT_DIR[:-1]+" -rm")
    print "complete!  \n"
    
def shell():
    exit = False
    while not exit:
        cmd = raw_input("shell>")
        
        if cmd == "exit":
            exit = True
            print("Bye!")
        elif cmd[0:6] == "search":
            arg = cmd.split(" ")
            print("You typed search "+arg[1])
        else:
            print("'"+cmd+"' not found.")

def parse_args():

    parser = optparse.OptionParser('Usage [-f <Music file>][-z][-s]')

    parser.add_option('-f', dest='file', type='string', \
                        help='music file')
    parser.add_option('-z', dest='rar', action="store_true", \
                        help='Makes a zip file for the output')
    parser.add_option('-s', dest='shell', action="store_true", \
                        help='Displays a shell')

    (options, args) = parser.parse_args()

    file = options.file
    rar = options.rar
    shell = options.shell
    
    if file == None:
        file = FILE
    if rar == None:
        rar = RAR

    return rar, file, shell


def main():
    (RAR, FILE, SHELL) = parse_args()
    if SHELL:
        shell()
    else:
        parse_file()
        make_dirs()
        song_n = len(songs)

        for i, song in enumerate(songs):
            print str(i)+"/"+str(song_n)+" ["+str((i*100)/song_n)+"%] "+song
            url = get_link(song)
            audio = get_audio(url)
            download_mp3(audio, song)

        if RAR:
            zip_dir()

if __name__ == '__main__':
    main()
