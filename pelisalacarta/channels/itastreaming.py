# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para itastreaming
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
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

__channel__ = "itastreaming"
__category__ = "F"
__type__ = "generic"
__title__ = "itastreaming"
__language__ = "IT"

COOKIEFILE = "/Users/arturo/itacookie.lwp"
h = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:37.0) Gecko/20100101 Firefox/37.0'}
baseUrl = "http://itastreaming.co"

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
    logger.info("pelisalacarta.itastreaming  mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__ , action="movies", title="ultimi film inseriti..." , url="http://itastreaming.co" ))
    itemlist.append( Item(channel=__channel__ , action="search", title="Cerca Film"))
    itemlist.append( Item(channel=__channel__ , action="movies", title="animazione" , url="http://itastreaming.co/genere/animazione" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="avventura" , url="http://itastreaming.co/genere/avventura" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="azione" , url="http://itastreaming.co/genere/azione" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="biografico" , url="http://itastreaming.co/genere/biografico" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="comico" , url="http://itastreaming.co/genere/comico" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="commedia" , url="http://itastreaming.co/genere/commedia" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="documentario" , url="http://itastreaming.co/genere/documentario" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="drammatico" , url="http://itastreaming.co/genere/drammatico" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="erotico" , url="http://itastreaming.co/genere/erotico" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="fantascienza" , url="http://itastreaming.co/genere/fantascienza" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="fantasy" , url="http://itastreaming.co/genere/fantasy" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="gangstar" , url="http://itastreaming.co/genere/gangstar" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="giallo" , url="http://itastreaming.co/genere/giallo" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="guerra" , url="http://itastreaming.co/genere/guerra" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="horror" , url="http://itastreaming.co/genere/horror" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="musical" , url="http://itastreaming.co/genere/musical" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="romantico" , url="http://itastreaming.co/genere/romantico" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="storico" , url="http://itastreaming.co/genere/storico" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="thriller" , url="http://itastreaming.co/genere/thriller" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="western" , url="http://itastreaming.co/genere/western" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="HD" , url="http://itastreaming.co/qualita/hd" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="DVD-RIP" , url="http://itastreaming.co/qualita/dvdripac3" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="CAM" , url="http://itastreaming.co/qualita/cam" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="HD-MD" , url="http://itastreaming.co/qualita/hd-md" ))
    itemlist.append( Item(channel=__channel__ , action="movies", title="HD-TS" , url="http://itastreaming.co/qualita/hd-ts" ))

    return itemlist

#searching for films
def search(item, text):

    itemlist = []
    text = text.replace(" ", "%20")
    item.url = "http://itastreaming.co/?s=" + text

    try:

        #dcap = dict(DesiredCapabilities.PHANTOMJS)
        #dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:37.0) Gecko/20100101 Firefox/37.0")
        #browser = webdriver.PhantomJS(executable_path='/bin/phantomjs',desired_capabilities = dcap, service_log_path=os.path.devnull)
        #browser.get(item.url)
        #time.sleep(5)
        #data =  browser.page_source.encode('utf-8')

        biscotto = cookielib.MozillaCookieJar()
        biscotto.load(COOKIEFILE)
        data = requests.get(item.url, cookies=biscotto, headers=h)
        data = data.text.encode('utf-8')
        data = data.replace('&#8211;','-').replace('&#8217;',' ')
        pattern = '<img class="imx" style="margin-top:0px;" src="?([^>"]+)"?.*?alt="?([^>"]+)"?.*?'
        pattern += '<h3><a href="?([^>"]+)"?.*?</h3>'
        matches = re.compile(pattern,re.DOTALL).findall(data)

        for scrapedthumbnail, scrapedtitle, scrapedurl in matches:
            title = scrapedtitle.strip()
            url = urlparse.urljoin(item.url, scrapedurl)
            #thumbnail = urlparse.urljoin(item.url, scrapedthumbnail)
            thumbnail = scrapthumb(title)
            itemlist.append(Item(channel=__channel__, action="grabing", title=title, url=url, thumbnail=thumbnail, folder=True))

        return itemlist

    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


#azione "movies" server per estrerre i titoli
def movies(item):

    createCookies()
    itemlist = []

    #dcap = dict(DesiredCapabilities.PHANTOMJS)
    #dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:37.0) Gecko/20100101 Firefox/37.0")
    #browser = webdriver.PhantomJS(executable_path='/bin/phantomjs',desired_capabilities = dcap, service_log_path=os.path.devnull)
    #browser.get(item.url)
    #time.sleep(5)
    #data =  browser.page_source.encode('utf-8')

    biscotto = cookielib.MozillaCookieJar()
    biscotto.load(COOKIEFILE)
    data = requests.get(item.url, cookies=biscotto, headers=h)
    data = data.text.encode('utf-8')
    data = data.replace('&#8211;','-').replace('&#8217;',' ')
    patron  = '<div class="item">\s*'
    patron += '<a href="?([^>"]+)"?.*?title="?([^>"]+)"?.*?'
    patron += '<div class="img">\s*'
    patron += '<img.*?src="([^>"]+)'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if not matches:
        print "Coockies expired!, delete it"
        os.remove(COOKIEFILE)
    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = scrapthumb(title)
        scrapedplot = ""
        itemlist.append( Item(channel=__channel__, action="grabing", title=title , url=url , thumbnail=thumbnail , plot=scrapedplot , folder=True) )

    #next page
    patternpage = '<a rel="nofollow" class="previouspostslink\'" href="(.*?)">Seguente \›</a>'
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
    #dcap = dict(DesiredCapabilities.PHANTOMJS)
    #dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:37.0) Gecko/20100101 Firefox/37.0")
    #browser = webdriver.PhantomJS(executable_path='/bin/phantomjs',desired_capabilities = dcap, service_log_path=os.path.devnull)
    #browser.get(item.url)
    #time.sleep(5)
    #data =  browser.page_source.encode('utf-8')
    biscotto = cookielib.MozillaCookieJar()
    biscotto.load(COOKIEFILE)
    data = requests.get(item.url, cookies=biscotto, headers=h)
    data = data.text.encode('utf-8')

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



def scrapthumb(title):

    title = title.strip().replace('–','').replace('’','-').replace('à','a')
    title = title.replace(' ','-')
    title = title[:-7]
    #print title
    mdburl = 'https://www.themoviedb.org/search?query=' + title
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
        print "thumb not found for: " + mdburl

    return thumbnail
