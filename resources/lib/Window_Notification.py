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

LINE_CHARS = 70
MAX_LINE_CHARS = 75
CLOSE_TIMEOUT = 6

MEDIA_RESOURCE_PATH = xbmc.translatePath( 'special://home/scripts/xbtweet/resources/skins/Default/media' )


### The adding button Code  (only really need this bit)
def setupButtons(self,x,y,w,h,a="Vert",f=None,nf=None):
    self.numbut  = 0
    self.butx = x
    self.buty = y
    self.butwidth = w
    self.butheight = h
    self.butalign = a
    self.butfocus_img = f
    self.butnofocus_img = nf
 
def addButon(self,text):
    if self.butalign == "Hori":
        c =  xbmcgui.ControlButton(self.butx + (self.numbut * self.butwidth),self.buty,self.butwidth,self.butheight,text)
        self.addControl(c)
    elif self.butalign == "Vert":
        c = xbmcgui.ControlButton(self.butx ,self.buty + (self.numbut * self.butheight),self.butwidth,self.butheight,text)
        self.addControl(c)
    self.numbut += 1
    return c
### The End of adding button Code 

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
                self.ui.getControl( CONTROL_CLOSE_BUTTON ).setLabel(__language__(30052) + '(' +str( self.maxcount-i ) + ')')
                time.sleep(1)
                if (i == self.maxcount):
                    self.ui.exit_script()
                if (stoptimer):
                    self.ui.getControl( CONTROL_CLOSE_BUTTON ).setLabel(__language__(30052))
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
    
    terminate = False
    stoptimer = False
    twittertext = "TWITTER TEXT"
    dialogtype = "mention"
    tweetsource = ""
    tweetsourceimage = "twitterpic.png"
    
    def __init__( self, *args, **kwargs):
        pass

    def onInit( self ):
        global twittertext
        global tweetsourceimage
        global tweetfromstring
        
        self.getControl( CONTROL_REPLY_BUTTON ).setLabel( __language__(30053) )
        self.getControl( CONTROL_TWITTER_FROM ).setLabel( tweetfromstring )
        self.getControl( CONTROL_TWITTER_TEXT ).setLabel( twittertext )        
        self.getControl( CONTROL_TWITTER_IMAGE ).setImage ( tweetsourceimage )
        
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

    def setTwitterText(self, text, dtype, tsource, tsourceimage, tcreatedat, tappsource):
        global twittertext
        global tweetsource
        global tweetsourceimage
        global tweetcreatedat
        global tweetappsource
        global tweetfromstring
        global dialogtype
        
        dialogtype = dtype
        tweetsource = tsource
        twittertext = text
        tweetsourceimage = tsourceimage
        tweetcreatedat = tcreatedat
        tweetappsource = tappsource

        dt2 = datetime.datetime.utcnow()
        dateDiff = dt2 - tweetcreatedat
        if dialogtype == 'mention':
            tweetfromstring = tsource + ' - ' + str(dateDiff.seconds / 60) + ' ' + __language__(30055) + ' ' + tweetappsource
        if dialogtype == 'direct_message':
            tweetfromstring = __language__(30057) + ' ' + tsource + ' - ' + str(dateDiff.seconds / 60) + ' ' + __language__(30056)
        
        if len(twittertext) > LINE_CHARS:
            splitindex = twittertext.find(' ', LINE_CHARS)
            if splitindex >= MAX_LINE_CHARS:
                splitindex = twittertext.find(' ', LINE_CHARS-10)
            twittertext = twittertext[0:splitindex] + '[CR]' + twittertext[splitindex+1:len(twittertext)]
        #twittertext = text
    
