from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib.error


def clear_lyrics():
    file = open('data/lyrics.txt', 'w').close()


def get_songs(site, artist):
    hdr = {'User-Agent': 'Mozilla/5.0'}

    songs_file = open('data/{}-songs.txt'.format(artist), 'w+')

    i = 1
    while True:
        try:
            req = Request(site.format(i), headers=hdr)
            page = urlopen(req)

            if page.geturl() != site.format(i):
                break

            soup = BeautifulSoup(page, 'html.parser')

            songs = soup.find_all('div', attrs={'class': 'title'})

            for song in songs:
                song = song.findChildren('a')[0].encode_contents().decode('utf-8')
                song = song.lower()
                song = song.replace(' ', '-')

                songs_file.write(song + "\n")

            i += 1
        except:
            break


def get_songs_mac_miller():
    get_songs("https://www.allmusic.com/artist/mac-miller-mn0002653603/songs/all/{}", 'mac-miller')


def get_songs_eminem():
    get_songs("https://www.allmusic.com/artist/eminem-mn0000157676/songs/all/{}", 'eminem')


def get_lyrics(filename, artist):
    site = 'http://metrolyrics.com/{}-lyrics-' + artist + '.html'
    filename_output = 'data/lyrics.txt'
    output = open(filename_output, 'a')

    songs = open(filename).read()

    for song in songs.split("\n"):
        try:
            if song == '':
                break

            page = urlopen(site.format(song))
            soup = BeautifulSoup(page, 'html.parser')
            verses = soup.find_all('p', attrs={'class': 'verse'})

            lyrics = ''

            for verse in verses:
                text = verse.text.strip()
                for char in text:
                    if len(lyrics) > 0 and char.isupper() and lyrics[-1].islower():
                        lyrics += '\n'
                    lyrics += char

            if len(lyrics) == 0:
                print('Did not find {}'.format(song))
            else:
                print('saving {} with {} words'.format(song, len(lyrics)))
                output.write(lyrics + "\n\n")

        except:
            print('Did not find {}'.format(song))

    output.close()


if __name__ == '__main__':
    get_songs_mac_miller()
    get_songs_eminem()
    clear_lyrics()
    get_lyrics('data/mac-miller-songs.txt', 'mac-miller')
    get_lyrics('data/eminem-songs.txt', 'eminem')
