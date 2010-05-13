import sys
import os
import xbmc
import string
import simplejson as json
import urllib
import urllib2

__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/scripts/trakt/"
__version__ = "0.0.1"

#Path handling
LANGUAGE_RESOURCE_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'language' ) )
CONFIG_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'settings.cfg' ) )
AUTOEXEC_PATH = xbmc.translatePath( 'special://home/scripts/autoexec.py' )
VERSION_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'version.cfg' ) )

#Consts
AUTOEXEC_SCRIPT = '\nimport time;time.sleep(5);xbmc.executebuiltin("XBMC.RunScript(special://home/scripts/trakt/default.py,-startup)")\n'

__language__ = xbmc.Language( os.getcwd() ).getLocalizedString
__settings__ = xbmc.Settings( path=os.getcwd() )

def SendUpdate(info, sType):
    Debug("Creating data to send", False)
    # split on type and create data packet for each type
    if (sType == "Movie"):
        Debug("Parsing Movie", False)
        # format: title, year
        title, year = info.split(",")
        toSend = urllib.urlencode({"type": sType, "title": title, "year": year})
    elif (sType == "TVShow"):
        Debug("Parsing TVShow", False)
        # format: title, year, season, episode
        title, year, season, episode = info.split(",")
        toSend = urllib.urlencode({"type": sType, "title": title, "year": year, "season": season, "episode": episode})
        
    Debug("Data: "+toSend, False)
    
    # send
    transmit(toSend)
    
def transmit(status):
    
    def basic_authorization(user, password):
        s = user + ":" + password
        return "Basic " + s.encode("base64").rstrip()

    req = urllib2.Request("http://www.theshallo.ws/trakt/index.php",
            status,
            headers = { "Accept": "*/*",   
                        "User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)", 
                      })

    f = urllib2.urlopen(req)
    # TODO : add error handling

def Debug(message, Verbose=True):
    bVerbose = __settings__.getSetting( "debug" )
    if (bVerbose == 'true'):
        bVerbose = True
    else:
        bVerbose = False
    
    if (bVerbose and Verbose):
        # repr() is used, got wierd issues with unicode otherwise, since we send mixed string types (eg: unicode and ascii) 
        print repr(message)
    elif (not Verbose):
        # repr() is used, got wierd issues with unicode otherwise, since we send mixed string types (eg: unicode and ascii) 
        print repr(message)

def CheckVersion():
    Version = ""
    if (os.path.exists(VERSION_PATH)):
        versionfile = file(VERSION_PATH, 'r')
        Version = versionfile.read()        
    return Version

def WriteVersion(Version):
    print Version
    print VERSION_PATH
    versionfile = file(VERSION_PATH, 'w')
    versionfile.write (Version)
    versionfile.close()

def CheckIfFirstRun():
    global CONFIG_PATH
    if (os.path.exists(CONFIG_PATH)):
        return False
    else:
        return True
    
def CheckIfUpgrade():
    return False

def CalcPercentageRemaining(currenttime, duration):
    try:
         iCurrentMinutes = (int(currenttime.split(':')[0]) * 60) + int(currenttime.split(':')[1])
    except:
        iCurrentMinutes = int(0)
        
    try:
        iDurationMinutes = (int(duration.split(':')[0]) * 60) + int(duration.split(':')[1])
    except:
        iDurationMinutes = int(0)

    try:
        Debug( 'Percentage of progress: ' + str(float(iCurrentMinutes) / float(iDurationMinutes)), True)
        return float(iCurrentMinutes) / float(iDurationMinutes) 
    except:
        Debug( 'Percentage of progress: null', True)
        return float(0.0)

def SetAutoStart(bState = True):
    Debug( '::AutoStart::' + str(bState), True)
    if (os.path.exists(AUTOEXEC_PATH)):
        Debug( 'Found Autoexec.py file, checking we''re there', True)
        bFound = False
        autoexecfile = file(AUTOEXEC_PATH, 'r')
        filecontents = autoexecfile.readlines()
        autoexecfile.close()
        for line in filecontents:
            if line.find('trakt') > 0:
                Debug( 'Found our script, no need to do anything', True)
                bFound = True
        if (not bFound):
            Debug( 'Appending our script to the autoexec.py script', True)
            autoexecfile = file(AUTOEXEC_PATH, 'w')
            filecontents.append(AUTOEXEC_SCRIPT)
            autoexecfile.writelines(filecontents)            
            autoexecfile.close()
        if (bFound and not bState):
            #remove line
            Debug( 'Removing our script from the autoexec.py script', True)
            autoexecfile = file(AUTOEXEC_PATH, 'w')
            for line in filecontents:
                if not line.find('xbTweet') > 0:
                    autoexecfile.write(line)
            autoexecfile.close()            
    else:
        Debug( 'File Autoexec.py is missing, creating file with autostart script', True)
        autoexecfile = file(AUTOEXEC_PATH, 'w')
        autoexecfile.write (AUTOEXEC_SCRIPT.strip())
        autoexecfile.close()
    Debug( '::AutoStart::'  , True)

#Check for new version
# if __settings__.getSetting( "new_ver" ) == "true":
#     try:
#         import re
#         import urllib
#         if not xbmc.getCondVisibility('Player.Paused') : xbmc.Player().pause() #Pause if not paused	
#         usock = urllib.urlopen(__svn_url__ + "default.py")
#         htmlSource = usock.read()
#         usock.close()
# 
#         version = re.search( "__version__.*?[\"'](.*?)[\"']",  htmlSource, re.IGNORECASE ).group(1)
#         Debug ( "SVN Latest Version :[ "+version+"]", True)
#         
#         if version > __version__:
#             import xbmcgui
#             dialog = xbmcgui.Dialog()
#             selected = dialog.ok(__language__(30002) % (str(__version__)),__language__(30003) % (str(version)),__language__(30004))
#     except:
#         print 'Exception in reading SVN'
