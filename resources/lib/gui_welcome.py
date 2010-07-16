import xbmc
import xbmcgui
import time
import threading
import os

__language__ = xbmc.Language( os.getcwd() ).getLocalizedString


EXIT_SCRIPT = ( 6, 10, 247, 275, 61467, 216, 257, 61448, )
CANCEL_DIALOG = EXIT_SCRIPT + ( 216, 257, 61448, 61467 ,)

CONTROL_CLOSE_BUTTON = 1001
CONTROL_DONTSHOW_BUTTON = 1007
CONTROL_HEADER_TEXT = 3001
CONTROL_MESSAGE_TEXT = 3002

class GUI( xbmcgui.WindowXMLDialog ):
    class CloseCounter(threading.Thread):
        def __init__(self, ui, maxcount):
            threading.Thread.__init__(self)
            self.maxcount = maxcount
            self.ui = ui
        def run(self):
            i = 0
            while (i < self.maxcount) and (not self.ui.terminate):
                i = i+1
                time.sleep(1)
                if (i == self.maxcount):
                    self.ui.close()
                if (stoptimer):
                    break
                
    def __init__( self, *args, **kwargs):
        self.terminate = False
        pass

    def onInit( self ):
        self.getControl( CONTROL_DONTSHOW_BUTTON ).setLabel( __language__(30051) )
        self.getControl( CONTROL_CLOSE_BUTTON ).setLabel( __language__(30052) )        
        
        self.getControl( CONTROL_HEADER_TEXT ).setLabel( self.headertext )
        self.getControl( CONTROL_MESSAGE_TEXT ).setText( self.message )        

        #counter = self.CloseCounter(self, CLOSE_TIMEOUT)
        #counter.start()

    def exit_script(self):
        if (self.getControl( CONTROL_DONTSHOW_BUTTON ).isSelected()):
            __settings__ = xbmc.Settings( path=os.getcwd() )
            __settings__.setSetting( "showwhatsnew", 'false')
        self.close()
        self.terminate = True        

    def onClick( self, controlId ):
        if (controlId == CONTROL_CLOSE_BUTTON):
            self.exit_script()
     
    def onFocus( self, controlId ):
        pass
    
    def onAction( self, action ):
	if ( action.getButtonCode() in CANCEL_DIALOG ):
            self.exit_script()
    
    def setParams(self, dialogtype, headertext, message, closetimer):
        self.dialogtype = dialogtype
        self.headertext = headertext
        self.message = message
        self.closetimer = closetimer
        
        pass
