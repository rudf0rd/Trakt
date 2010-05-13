import sys
import os
import xbmc
import xbmcgui
import time
import datetime

from threading import *
from twitter_wrapper import *

__language__ = xbmc.Language( os.getcwd() ).getLocalizedString

EXIT_SCRIPT = ( 6, 10, 247, 275, 61467, 216, 257, 61448, )
CANCEL_DIALOG = EXIT_SCRIPT + ( 216, 257, 61448, 61467 ,)
CONTROL_CLOSE_BUTTON = 1001
CONTROL_REPLY_BUTTON = 1002
CONTROL_TWITTER_TEXT = 300
CONTROL_TWITTER_IMAGE = 301
CONTROL_TWITTER_FROM = 302

LINE_CHARS = 62
MAX_LINE_CHARS = 70
CLOSE_TIMEOUT = 10

WINDOW_START = 5
WINDOW_WIDTH = 650
WINDOW_HEIGHT = 100

MEDIA_RESOURCE_PATH = xbmc.translatePath( 'special://home/scripts/xbtweet/resources/skins/Default/media' )

SKIN_WIDTH = 650

class GUI( xbmcgui.WindowXMLDialog ):
    class CloseCounter(Thread):
        def __init__(self, ui, maxcount):
            Thread.__init__(self)
            self.maxcount = maxcount
            self.ui = ui
        def run(self):
            global terminate
            i = 0
            while (i < self.maxcount) and (not terminate):
                i = i+1
                time.sleep(1)
                if (i == self.maxcount):
                    self.ui.exit_script()
                if (stoptimer):
                    break
                
    global terminate
    global stoptimer
    global twittertext
    global dialogtype
    global tweetsource
    global tweetsourceimage

    global tweetcreatedat
    global tweetappsource
    global tweetfromstring
    global windowid
    
    terminate = False
    stoptimer = False
    twittertext = "TWITTER TEXT"
    dialogtype = "mention"
    tweetsource = ""
    tweetsourceimage = "twitterpic.png"
    tweetfromstring = ""
    windowid = 0
    
    def __init__( self, *args, **kwargs):
        pass

    def onInit( self ):
        global twittertext
        global tweetsourceimage
        global tweetfromstring
        global windowid
        
        self.getControl( 1 ).setPosition(self.getControl(1).getPosition()[0],WINDOW_START+(windowid*WINDOW_HEIGHT))
        
        self.getControl( CONTROL_TWITTER_FROM ).setLabel( tweetfromstring )
        self.getControl( CONTROL_TWITTER_TEXT ).setLabel( twittertext )        
        #self.getControl( CONTROL_TWITTER_IMAGE ).setImage ( tweetsourceimage )

        counter = self.CloseCounter(self, CLOSE_TIMEOUT)
        counter.start()
        
    def exit_script( self, restart=False ):
        self.close()		

    def onClick( self, controlId ):
        global terminate
        global stoptimer
        global dialogtype
        if (controlId == CONTROL_CLOSE_BUTTON):
            self.exit_script()
            terminate = True
        if (controlId == CONTROL_REPLY_BUTTON):
            stoptimer = True
            global tweetsource
            if (dialogtype == "mention"):
                update = '@' + tweetsource + ' '
            if (dialogtype == "direct_message"):
                update = 'D @' + tweetsource + ' '               
            UpdateStatus(update, True)
            terminate = True
            self.exit_script()
     
    def onFocus( self, controlId ):
        #print 'onFocus: ' + str(controlId)
        if (controlId == CONTROL_REPLY_BUTTON):
            global stoptimer
            stoptimer = True            
        
    def onAction( self, action ):
        #print 'OnAction' + str(action) + ', button code: ' + str(action.getButtonCode())
        global terminate
        #print CANCEL_DIALOG
	if ( action.getButtonCode() in CANCEL_DIALOG ):
            terminate = True
            self.exit_script()

    def setTwitterText(self, text, dtype, tsource, tsourceimage, tcreatedat, tappsource, posy):
        global twittertext
        global tweetsource
        global tweetsourceimage
        global tweetcreatedat
        global tweetappsource
        global tweetfromstring
        global dialogtype
        global windowid
                
        dialogtype = dtype
        tweetsource = tsource
        twittertext = text
        tweetsourceimage = tsourceimage
        tweetcreatedat = tcreatedat
        tweetappsource = tappsource
        windowid = posy
        
        dateDiff = datetime.datetime.utcnow() - datetime.datetime.utcnow()
        try:
            dt2 = datetime.datetime.utcnow()
            dateDiff = dt2 - tweetcreatedat
        except:
            pass
        if dialogtype == 'mention':
            tweetfromstring = tsource + ' - ' + str(dateDiff.seconds / 60) + ' ' + __language__(30055) + ' ' + tweetappsource
        if dialogtype == 'direct_message':
            tweetfromstring = __language__(30057) + ' ' + tsource + ' - ' + str(dateDiff.seconds / 60) + ' ' + __language__(30056)
        if dialogtype == 'tweet':
            tweetfromstring = tsource + ' - ' + str(dateDiff.seconds / 60) + ' ' + __language__(30055) + ' ' + tweetappsource


        if len(twittertext) > LINE_CHARS:
            splitindex = twittertext.find(' ', LINE_CHARS)
            if splitindex >= MAX_LINE_CHARS:
                splitindex = twittertext.find(' ', LINE_CHARS-10)
            twittertext = twittertext[0:splitindex] + '[CR]' + twittertext[splitindex+1:len(twittertext)]
            
        #if len(twittertext) >= MAX_LINE_CHARS:
        #    twittertext = twittertext[0:MAX_LINE_CHARS-3] + '...'
