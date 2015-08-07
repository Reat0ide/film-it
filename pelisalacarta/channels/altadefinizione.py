# -*- coding: utf-8 -*-
#------------------------------------------------------------
#------------------------------------------------------------
import selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#import cfscrape
import time
#from pyvirtualdisplay import Display
import urlparse,urllib2,urllib,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc
import os, sys
from core import logger
from core import config
from core import scrapertools
from core.item import Item
#from servers import servertools
import json

__channel__ = "altadefinizione"
__category__ = "F"
__type__ = "generic"
__title__ = "altadefinizione"
__language__ = "IT"

def isGeneric():
    return True


def mainlist(item):
    
    #http://altadefinizione.click/film/avventura/
    itemlist = []
    itemlist.append( Item(channel=__channel__ , action="movies", title="ultimi film inseriti..." , url="http://altadefinizione.click" ))
    itemlist.append( Item(channel=__channel__ , action="search", title="Cerca Film"))
    itemlist.append( Item(channel=__channel__ , action="movies", title="animazione" , url="http://altadefinizione.click/film/animazione" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="avventura" , url="http://altadefinizione.click/film/avventura" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="azione" , url="http://altadefinizione.click/film/azione" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="biografico" , url="http://altadefinizione.click/film/biografico" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="comico" , url="http://altadefinizione.click/film/comico" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="commedia" , url="http://altadefinizione.click/film/commedia" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="crimine" , url="http://altadefinizione.click/film/crimine" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="documentario" , url="http://altadefinizione.click/film/documentario" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="drammatico" , url="http://altadefinizione.click/film/drammatico" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="erotico" , url="http://altadefinizione.click/film/erotico" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="familiare" , url="http://altadefinizione.click/film/familiare" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="fantascienza" , url="http://altadefinizione.click/film/fantascienza" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="fantasy" , url="http://altadefinizione.click/film/fantasy" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="gangstar" , url="http://altadefinizione.click/film/gangstar" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="gangstar" , url="http://altadefinizione.click/film/gangstar" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="guerra" , url="http://altadefinizione.click/film/guerra" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="horror" , url="http://altadefinizione.click/film/horror" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="mistero" , url="http://altadefinizione.click/film/mistero" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="musical" , url="http://altadefinizione.click/film/musical" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="noir" , url="http://altadefinizione.click/film/noir" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="romantico" , url="http://altadefinizione.click/film/romantico" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="sportivo" , url="http://altadefinizione.click/film/sportivo" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="storico" , url="http://altadefinizione.click/film/storico" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="thriller" , url="http://altadefinizione.click/film/thriller" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="western" , url="http://altadefinizione.click/film/western" ))


    return itemlist

def search(item, text):

    itemlist = []
    text = text.replace(" ", "%20")
    item.url = "http://altadefinizione.click/?s=" + text

    try:

        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:37.0) Gecko/20100101 Firefox/37.0")
        browser = webdriver.PhantomJS(executable_path='/bin/phantomjs',desired_capabilities = dcap, service_log_path=os.path.devnull)
        browser.get(item.url)
        time.sleep(5)
        data =  browser.page_source.encode('utf-8')

        pattern = '<div class="col-lg-3 col-md-3 col-xs-3">\s*'
        pattern += '<a href="(.*?)".*?alt="(.*?)"'
        matches = re.compile(pattern,re.DOTALL).findall(data)
        print matches

        for scrapedurl, scrapedtitle in matches:
            url = urlparse.urljoin(item.url, scrapedurl)
            title = scrapedtitle.strip()
            #thumbnail = urlparse.urljoin(item.url, scrapedthumbnail)
            thumbnail = scrapthumb(title)
            itemlist.append(Item(channel=__channel__, action="grabing", title=title, url=url, thumbnail=thumbnail, folder=True))

        return itemlist

    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []








def movies(item):

    itemlist = []

    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:37.0) Gecko/20100101 Firefox/37.0")
    browser = webdriver.PhantomJS(executable_path='/bin/phantomjs',desired_capabilities = dcap, service_log_path=os.path.devnull)
    browser.get(item.url)
    time.sleep(5)
    data =  browser.page_source.encode('utf-8')

    pattern = '<h2 class="titleFilm"><a href="(.*?)">(.*?)</a>'

    matches = re.compile(pattern,re.DOTALL).findall(data)
    print matches

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = scrapthumb(title)
        #thumbnail = ""
        #print thumbnail
        scrapedplot = ""
        itemlist.append( Item(channel=__channel__, action="grabing", title=title , url=url , thumbnail=thumbnail , plot=scrapedplot , folder=True) )

    #next page
    patternpage = '<a class="next page-numbers" href="?([^>"]+)">Succ.*?</a>'
    matches = re.compile(patternpage,re.DOTALL).findall(data)
    #print matches

    if not matches:
		patternpage = "<span class='current'.*?</span>"
		patternpage += "<a rel='nofollow' class='page larger' href='([^']+)'>.*?</a>"
		matches = re.compile(patternpage,re.DOTALL).findall(data)

    #print matches


    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="movies", title="Next Page >>" , url=scrapedurl , folder=True) )


    return itemlist

def grabing(item):

    itemlist = []
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:37.0) Gecko/20100101 Firefox/37.0")
    browser = webdriver.PhantomJS(executable_path='/bin/phantomjs',desired_capabilities = dcap, service_log_path=os.path.devnull)
    browser.get(item.url)
    time.sleep(5)
    data =  browser.page_source.encode('utf-8')


    #esegue questa funziona solo se si clicca sul titolo del film
    if item.title:
        filmtitle = str(item.title)
        filmtitle =  filmtitle.replace('–','')

        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:37.0) Gecko/20100101 Firefox/37.0")
        browser = webdriver.PhantomJS(executable_path='/bin/phantomjs',desired_capabilities = dcap, service_log_path=os.path.devnull)
        browser.get(item.url)
        time.sleep(7)
        try:
            nData = browser.execute_script("return nData")
            print nData
            for block in nData:
                itemlist.append( Item(channel=__channel__, action="playit", title=filmtitle + "  quality: " + block['width'] +  " x " + block['height'] , url=block['url'] ))
            browser.close()

        except:

            fakeurl = re.findall('"((http)s?://.*?hdpass.link.*?)"', data)
            print fakeurl

            url =  fakeurl[0][0]
            browser.get(url)
            time.sleep(7)
            nData = browser.execute_script("return nData")
            print nData
            print filmtitle
            for block in nData:
                print block['url']
                itemlist.append( Item(channel=__channel__, action="playit", title=filmtitle + "  quality: " + block['width'] +  " x " + block['height'] , url=block['url'] ))
            browser.close()

    return itemlist


def playit(item):

    itemlist = []
    print item.url
    itemlist.append( Item(channel=__channel__, action="playit", title=item.title , url=item.url ))
    if not xbmc.Player().isPlayingVideo():
        xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(item.url)
    return itemlist




#TO DO!!
def scrapthumb(title):

    title = re.sub('[^a-zA-Z0-9\n\.]', ' ', title)
    title = title.replace(' ','-')
    print title

    mdburl = 'https://www.themoviedb.org/search?query=' + title
    imdb = 'http://www.imdb.com/find?q=' + title                #il+fidanzato+di+mia++++sorella
    req = urllib2.Request(mdburl)
    response = urllib2.urlopen(req)
    data = response.read()
    pattern = '<div class="poster">\s*'
    pattern += '<a.*?src="(.*?)"'

    matches = re.compile(pattern,re.DOTALL).findall(data)
    thumbnail = ""

    if matches:
        thumbnail = matches[0]
        thumbnail = thumbnail.replace('w92','original')
    else:

        print "thumb not found on tmdb: " + mdburl
        #http://www.mymovies.it/database/ricerca/?q3=antboy

    return thumbnail