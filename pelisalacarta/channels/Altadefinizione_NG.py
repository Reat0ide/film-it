# -*- coding: utf-8 -*-
#------------------------------------------------------------
#------------------------------------------------------------
import selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import urlparse,urllib2,urllib,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc
import os, sys
from core import logger
from core import config
from core import scrapertools
from core.item import Item
import cookielib
import requests
import os.path

__channel__ = "altadefinizione_NG"
__category__ = "F"
__type__ = "generic"
__title__ = "altadefinizione_NG"
__language__ = "IT"

COOKIEFILE = "/Users/arturo/alta_NGcookie.lwp"
h = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:37.0) Gecko/20100101 Firefox/37.0'}
baseUrl = "http://altadefinizione.co"

def createCookies():

    if not os.path.isfile(COOKIEFILE):

        print "File not exists"
        #get cookies!
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:37.0) Gecko/20100101 Firefox/37.0")
        browser = webdriver.PhantomJS(executable_path='/bin/phantomjs',desired_capabilities = dcap, service_log_path=os.path.devnull)
        browser.get(baseUrl)
        time.sleep(10)
        a = browser.get_cookies()
        print 'Got cloudflare cookies:\n'
        browser.close()
        b = cookielib.MozillaCookieJar()

        for i in a:
            # create the cf_session_cookie
            ck = cookielib.Cookie(name=i['name'], value=i['value'], domain=i['domain'], path=i['path'], secure=i['secure'], rest=False, version=0,port=None,port_specified=False,domain_specified=False,domain_initial_dot=False,path_specified=True,expires=i['expiry'],discard=True,comment=None,comment_url=None,rfc2109=False)
            b.set_cookie(ck)
        # save into a file
        print b
        b.save(filename=COOKIEFILE, ignore_discard=True, ignore_expires=False)

    else:
        print "found it, do nothing!"
        b = True

    return b


def isGeneric():
    return True


def mainlist(item):

    itemlist = []
    itemlist.append( Item(channel=__channel__ , action="movies", title="ultimi film inseriti..." , url="http://altadefinizione.co/news" ))
    itemlist.append( Item(channel=__channel__ , action="search", title="Cerca Film"))
    itemlist.append( Item(channel=__channel__ , action="movies", title="animazione" , url="http://altadefinizione.co/genere/animazione" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="avventura" , url="http://altadefinizione.co/genere/avventura" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="azione" , url="http://altadefinizione.co/genere/azione" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="biografico" , url="http://altadefinizione.co/genere/biografico" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="commedia" , url="http://altadefinizione.co/genere/commedia" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="corto" , url="http://altadefinizione.co/genere/corto" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="documentario" , url="http://altadefinizione.co/genere/documentario" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="drammatico" , url="http://altadefinizione.co/genere/drammatico" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="erotico" , url="http://altadefinizione.co/genere/erotico" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="fantascienza" , url="http://altadefinizione.co/genere/fantascienza" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="fantasy" , url="http://altadefinizione.co/genere/fantasy" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="giallo" , url="http://altadefinizione.co/genere/giallo" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="guerra" , url="http://altadefinizione.co/genere/guerra" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="horror" , url="http://altadefinizione.co/genere/horror" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="musicale" , url="http://altadefinizione.co/genere/musicale" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="romantico" , url="http://altadefinizione.co/genere/romantico" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="storico" , url="http://altadefinizione.co/genere/storico" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="thriller" , url="http://altadefinizione.co/genere/thriller" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="western" , url="http://altadefinizione.co/genere/western" ))


    return itemlist


def search(item, text):
    createCookies()
    itemlist = []
    text = text.replace(" ", "%20")
    item.url = "http://altadefinizione.co/?s=" + text

    try:

        biscotto = cookielib.MozillaCookieJar()
        biscotto.load(COOKIEFILE)
        data = requests.get(item.url, cookies=biscotto, headers=h)
        data = data.text.encode('utf-8')
        print data
        pattern = '<div class="item cap-left">\s*'
        pattern += '<a href="(.*?)">\s*'
        pattern += '<div class="image">\s*'
        pattern += '<img src="(.*?)".*?alt="(.*?)"'
        matches = re.compile(pattern,re.DOTALL).findall(data)
        print matches
        for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
            url = urlparse.urljoin(item.url, scrapedurl)
            title = scrapedtitle.strip()

            thumbnail = scrapthumb(title)
            itemlist.append(Item(channel=__channel__, action="grabing", title=title, url=url, thumbnail=thumbnail, folder=True))

        return itemlist

    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []



def movies(item):

    createCookies()
    itemlist = []
    biscotto = cookielib.MozillaCookieJar()
    biscotto.load(COOKIEFILE)
    data = requests.get(item.url, cookies=biscotto, headers=h)
    data = data.text.encode('utf-8')
    data = data.replace('&#8211;','-').replace('&#8217;',' ').replace('&#8230;','...')

    pattern = '<div class="item cap-left">\s*'
    pattern += '<a href="(.*?)">\s*'
    pattern += '<div class="image">\s*'
    pattern += '<img src="(.*?)".*?alt="(.*?)"'
    matches = re.compile(pattern,re.DOTALL).findall(data)

    print matches
    if not matches:
        print "Coockies expired!, delete it"
        os.remove(COOKIEFILE)

    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Scraping Titles.')
    i = 0
    for scrapedurl,scrapedthumbnail, scrapedtitle in matches:
        title = scrapedtitle.strip()
        message = "Scraping movies - " + str(i) + " : " + title
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = scrapthumb(title)

        scrapedplot = ""
        itemlist.append( Item(channel=__channel__, action="grabing", title=title , url=url , thumbnail=thumbnail , plot=scrapedplot , folder=True) )
        progress.update( int(i) , "", message, "" ) #BAR
        xbmc.sleep( 1000 ) #BAR
        i = i + 1
    progress.close()

    patternpage = '<link rel="next" href="(.*?)"'
    matches = re.compile(patternpage,re.DOTALL).findall(data)
    print matches


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
    browser.find_element_by_link_text("HD").click()
    #time.sleep(3)
    data =  browser.page_source.encode('utf-8')
    #print data

    #esegue questa funziona solo se si clicca sul titolo del film
    if item.title:
        filmtitle = str(item.title)
        filmtitle =  filmtitle.replace('–','')
        thumbnail = scrapthumb(filmtitle)
        try:
            nData = browser.execute_script("return theSources")
            print nData
            for block in nData:
                print block['file']
                itemlist.append( Item(channel=__channel__, action="playit", title=filmtitle + " quality: " + block['label'] , url=block['file'], thumbnail=thumbnail ))
            browser.close()

        except:

            print "file not found"

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

    #mdburl = 'https://www.themoviedb.org/search?query=' + title
    mdburl = 'https://www.themoviedb.org/search/movie?query=' + title
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