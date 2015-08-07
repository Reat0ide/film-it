# -*- coding: utf-8 -*-
#------------------------------------------------------------

import urllib2,urllib,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc

from urlparse import urlparse
from urlparse import urljoin

import selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os, sys
from core import logger
from core import config
from core import scrapertools
from core.item import Item

from t0mm0.common.net import Net
import urlresolver




__channel__ = "cb01"
__category__ = "F"
__type__ = "generic"
__title__ = "cb01"
__language__ = "IT"

#DEBUG = config.get_setting("debug")
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:20.0) Gecko/20100101 Firefox/20.0"


def isGeneric():
    return True

def mainlist(item):

    itemlist = []
    itemlist.append( Item(channel=__channel__ , action="ultimi", title="Ultimi 100 Film aggiornati" , url="http://www.cb01.eu/lista-film-ultimi-100-film-aggiornati/" ))
    itemlist.append( Item(channel=__channel__ , action="search", title="Cerca Film"))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Ultimi Film aggiunti" , url="http://www.cb01.eu/" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Avventura" , url="http://www.cb01.eu/category/avventura-aggiornato/" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Azione" , url="http://www.cb01.eu/category/azione-aggiornato/" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Biografico" , url="http://www.cb01.eu/category/biografico-aggiornato/" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Comico" , url="http://www.cb01.eu/category/comico-aggiornato/" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Commedia" , url="http://www.cb01.eu/category/commedia-aggiornato/" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Documentario" , url="http://www.cb01.eu/category/documentario-aggiornato/" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Drammatico" , url="http://www.cb01.eu/category/drammatico-aggiornato/" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Erotico" , url="http://www.cb01.eu/category/erotico-aggiornato/" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Fantascienza" , url="http://www.cb01.eu/category/fantascienza-aggiornato/" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Fantasy" , url="http://www.cb01.eu/category/fantasy-fantastico-aggiornato/" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Gangstar" , url="http://www.cb01.eu/category/gangster-aggiornato/" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Grottesco" , url="http://www.cb01.eu/category/grottesco-aggiornato/" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Guerra" , url="http://www.cb01.eu/category/guerra-aggiornato/" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Horror" , url="http://www.cb01.eu/category/horror-aggiornato/" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Musical" , url="http://www.cb01.eu/category/musical-aggiornato/" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Noir" , url="http://www.cb01.eu/category/noir-aggiornato/" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Poliziesco" , url="http://www.cb01.eu/category/poliziesco-aggiornato/" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Sentimentale" , url="http://www.cb01.eu/category/sentimentale-aggiornato/" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Storico" , url="http://www.cb01.eu/category/storico-aggiornato/" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Thriller" , url="http://www.cb01.eu/category/thriller-aggiornato/" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Western" , url="http://www.cb01.eu/category/western-aggiornato/" ))


    itemlist.append( Item(channel=__channel__ , action="peliculas", title="HD-Altadefinizione" , url="http://www.cb01.eu/category/hd-alta-definizione/" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="HD-720" , url="http://www.cb01.eu/category/hd/hd-720p/" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="HD-1080" , url="http://www.cb01.eu/category/hd/hd-1080p/" ))


    return itemlist


def search(item, text):
    print "cerca"
    itemlist = []
    text = text.replace(" ", "%2B")
    print text
    item.url = "http://www.cb01.eu/?s=" + text
    try:
        print item.url
        data = scrapertools.cache_page(item.url)
        pattern = '<div class="span12 filmbox">\s*'
        pattern +='<div class="span4"> <a href="?([^>"]+)"?><p><img.*?src="([^>"]+)'
        matches = re.compile(pattern,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)

        for scrapedurl,scrapedthumbnail  in matches:
            url = scrapedurl
            title = urlparse(url)
            title = title.path
            thumbnail = ""

            itemlist.append(Item(channel=__channel__, action="grabing", title=title, url=url, thumbnail=thumbnail, folder=True))

        return itemlist

    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []




    return itemlist


def ultimi(item):

    print "lista ultimi film"
    #<td width="342" height="57" valign="top"><!-- Lista a/z - http://www.cineblog01.com --><strong>Ultimi 100 film Aggiornati:</a></strong><br>- <a href="http://www.cb01.eu/argo-2012/">Argo [HD] (2012)</a>
    itemlist = []

    data = scrapertools.cache_page(item.url)
    #pattern = '<td width="342" height="57" valign="top">.*?<a href="(.*?)">(.*?)</a>(.*?)'
    pattern = '<td width="342" height="57" valign="top">(.*?)</td>'
    matches = re.compile(pattern,re.DOTALL).findall(data)
    megastring = str(matches)
    megastring = megastring[2:-2]
    matches = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', megastring)

    for res in matches:
        # elimina il primo elemento!
        url = res
        title = urlparse(url)
        title = title.path
        #to do: searching for thumbnail
        thumbnail = ""
        itemlist.append( Item(channel=__channel__, action="grabing", title=title , url=url , thumbnail=thumbnail, folder=True) )


    return itemlist

#azione "peliculas" server per estrerre i titoli
def peliculas(item):
    print item.url + " URL Attuale"
    itemlist = []
    data = scrapertools.cache_page(item.url)

    pattern = '<div class="span12 filmbox">\s*'
    pattern +='<div class="span4"> <a href="?([^>"]+)"?><p><img.*?src="([^>"]+)'
    matches = re.compile(pattern,re.DOTALL).findall(data)
    #print matches
    for scrapedurl,scrapedthumbnail in matches:

        url = scrapedurl
        title = urlparse(url)
        title = title.path
        thumbnail = ""
        itemlist.append( Item(channel=__channel__, action="grabing", title=title , url=url , thumbnail=scrapedthumbnail, folder=True) )

    #next page
    patternpage = "<link rel='next' href=\'(.*?)\' />"
    res = re.compile(patternpage,re.DOTALL).findall(data)
    newurl = str(res)
    newurl = newurl[2:-2]
    print newurl + " next url"
    print res

    itemlist.append( Item(channel=__channel__, action="peliculas", title="Next Page >>" , url=newurl , folder=True) )


    return itemlist


def grabing(item):
    itemlist = []
    data = scrapertools.cache_page(item.url)

    pattern = '//((?:www.)?videomega.tv)/(?:(?:iframe|cdn|validatehash|view)\.php)?\?(?:ref|hashkey)=([a-zA-Z0-9]+)'
    matches = re.compile(pattern).findall(data)

    if matches:
        for res in matches:
            url = matches[0][0]
            media_id = matches[0][1]

        stream_url = urlresolver.HostedMediaFile(host= url, media_id=media_id).resolve()
        itemlist.append( Item(channel=__channel__, action="playit", title=item.title , url=stream_url ))

    elif not matches:
        #search for other medium
        try:
            stream_url = 'http://vkpass.com/'
            pattern = 'data-src="http://vkpass.com/(.*?)"'
            matches = re.compile(pattern).findall(data)
            print matches
            if matches:
                matches = matches[0]
                stream_url = stream_url + matches # vkpass encrypted url
                url = vkpass_streams(stream_url)
                print url # OK!!

                for quali,gurl in url:
                    itemlist.append( Item(channel=__channel__, action="playit", title=item.title + "  quality: " + quali , url=gurl ))
        except:
            print "medium not found"

    else:
        stream_url = 'http://swzz.xyz/link/'
        pattern = 'data-src="http://swzz.xyz/link/(.*?)"'
        matches = str(re.compile(pattern).findall(data))
        print matches









    return itemlist



def playit(item):
    itemlist = []
    print item.url
    itemlist.append( Item(channel=__channel__, action="playit", title=item.title , url=item.url ))
    if not xbmc.Player().isPlayingVideo():
        xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(item.url)

    return itemlist


def vkpass_streams(url):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': "http://cb01.eu/"
    }

    #print HEADERS

    req = urllib2.Request(url, headers=HEADERS)
    response = urllib2.urlopen(req)
    html = response.read()
    #print html
    response.close()

    return _vkpass_streams_from_html(html)


def _vkpass_streams_from_html(html):
    identifier = "vsource=["
    vsource_start = html.index(identifier) + len(identifier) - 1
    vsource_end = html.index("]", vsource_start + 1) + 1

    file_start = html.find('file:', vsource_start)
    formats = []

    while file_start != -1 and file_start < vsource_end:
        quote_start = file_start + 6
        quote_end = html.find('"', quote_start + 1)
        url = html[quote_start : quote_end]

        label_start = html.find('label:', quote_end)
        quote_start = label_start + 7
        quote_end = html.find('"', quote_start + 1)
        label = html[quote_start : quote_end]

        formats.append((label, url))
        file_start = html.find('file:', quote_end)


    return formats
