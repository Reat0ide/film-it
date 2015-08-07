# -*- coding: utf-8 -*-
#------------------------------------------------------------

#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys,xbmcplugin ,xbmcgui, xbmcaddon, xbmc

from core import scrapertools
from core import config
from core import logger
from core.item import Item
#from servers import servertools

__channel__ = "tengourl"
__category__ = "G"
__type__ = "generic"
__title__ = "tengourl"
__language__ = ""

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="search", title="Insert your URL"))

    return itemlist


def search(item,texto):
    
    itemlist = []
    url = texto+"|User-Agent=NSPlayer"
    if not xbmc.Player().isPlayingVideo():
        xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(url)

    return itemlist

