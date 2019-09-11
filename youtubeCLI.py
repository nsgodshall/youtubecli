import os 
import argparse
import requests
import time 
from bs4 import BeautifulSoup
from selenium import webdriver

def genArgparse():
    parser = argparse.ArgumentParser(prog='YoutubeCLI', usage='A command line tool to play youtube videos with no GUI interaction. Espicially useful for remote hosts.')
    parser.add_argument('-l', '--link', default='', help='URL of youtube video to be played')
    parser.add_argument('-a', '--autoplay', help='enable youtube autoplay, which is disabled by default', action="store_true")
    parser.add_argument('-u', '--ublock', help='toggle uBlock, which is enabled by default, uBlock must be installed in default Firefox directory: /home/user/.mozilla/firefox/dr28epq0.default/extensions/', action='store_true')
    parser.add_argument('-s', '--search', type=str, help='URL of youtube video to be played')
    args = parser.parse_args()
    return parser, args

def getSearchResults(query):
    page = requests.get('https://www.youtube.com/results?search_query={}'.format(query))
    soup = BeautifulSoup(page.content, 'html.parser')
    titles = soup.find_all("a", class_="yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link")
    videos = []
    for title in titles[:5]:
        videos.append((title.attrs['title'], title.attrs['href']))
    return videos

def videoSelector(videos):
    count = 1
    print('Which video do you want to play?')
    for video in videos:
        print('{}. {}'.format(count, video[0]))
        count += 1
    selection = int(input()) - 1 
    href = videos[selection][1]
    videoLink = 'https://youtube.com{}'.format(href)
    # os.system("clear")
    return videoLink

def playVideo(args, **kwargs):
    driver = webdriver.Firefox() #Establish Firefox driver, documentatin for installing geckodriver will need to be created 
    if args.ublock:
        user = os.getlogin()
        extensions_dir = '/home/{}/.mozilla/firefox/dr28epq0.default/extensions/'.format(user) #Default directectory of firefox extensions
        ublock = 'uBlock0@raymondhill.net.xpi'
        driver.install_addon(extensions_dir + ublock, temporary=True)
    if kwargs != {}:
        driver.get(kwargs['videoLink'])
    else: 
        driver.get(args.link)
    driver.find_element_by_id('ytd-player').click()
    time.sleep(1)
    if not args.autoplay:
        driver.find_element_by_id('toggleButton').click()   

parser, args = genArgparse()

if args.link != '':
    playVideo(args)

if args.search != '':
    videoList = getSearchResults(args.search)
    videoToPlay = videoSelector(videoList)
    playVideo(args, videoLink=videoToPlay)
