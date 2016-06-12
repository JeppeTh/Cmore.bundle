URLS = [{'site':'se', 'id':160000, 'lang':'sv_SE'},
        {'site':'no', 'id':160146, 'lang':'nb_NO'},
        {'site':'dk', 'id':162715, 'lang':'da_DK'}
        ]
# Services.Cmore.cSportsRoot: "{"no":"160146","se":"160000","dk":"162715"}",
# /cmore/query/asset/sport/{csports_root}/{language}?Country=
# 
Login = SharedCodeService.cmorelib.Login
MakeVideoObject = SharedCodeService.cmorelib.MakeVideoObject

VIDEO_PREFIX = "/video/cmore"

ART = 'art-default.jpg'
ICON = 'icon-default.png'
ICON_PREFS = 'icon-prefs.png'

IPAD_UA = 'Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X; en-us) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B176 Safari/7534.48.3'

MAX_LEN = 50

####################################################################################################

# This function is initially called by the PMS framework to initialize the plugin. This includes
# setting up the Plugin static instance along with the displayed artwork.
def Start():
    Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')
    Plugin.AddViewGroup('List', viewMode = 'List', mediaType = 'items')
    
    ObjectContainer.art = R(ART)
    ObjectContainer.title1 = L('Title')
    ObjectContainer.view_group = 'List'
    
    DirectoryObject.thumb = R(ICON)
    DirectoryObject.art = R(ART)
    VideoClipObject.thumb = R(ICON)
    VideoClipObject.art = R(ART)

    HTTP.CacheTime = CACHE_1HOUR
    HTTP.Headers['User-Agent'] = IPAD_UA

# This main function will setup the displayed items.
@handler(VIDEO_PREFIX, L('Title'), ICON)
def MainMenu():

    oc = ObjectContainer()
    try:
        Login()
        site = Prefs['site'].lower()
        start_url = "http://mobilemid-direkt.cmore.se/cmore/query/asset/sport/"
        for item in URLS:
            if site == item['site']:
                start_url = start_url + "%i/%s?Country=%s" % (item['id'], item['lang'], item['lang'])
                break
        oc.add(CreateDirObject("Sport", Callback(Category, title2="Sport", url=start_url)))
        oc.add(CreateDirObject("Re-Login", Callback(ReLogin)))
        oc.add(PrefsObject(title = L('Preferences Menu Title'), thumb=R(ICON_PREFS)))
    except Exception as e:
        oc.message = "Login failed"
        oc.add(CreateDirObject("Login", Callback(MainMenu)))
        oc.add(PrefsObject(title = L('Preferences Menu Title'), thumb = R(ICON_PREFS)))

    return oc

@route('/video/cmore/category')
def Category(title2, url):
    Log("JTDEBUG Category(%s %s)" % (title2, url))
    oc = ObjectContainer(title2=unicode(title2))
    for item in JSON.ObjectFromURL(url)['result']:
        oc.add(MakeVideoObject(url, item))
        if len(oc) >= MAX_LEN:
            break
    return oc

@route('/video/cmore/relogin', 'GET')
def ReLogin():
    Login(True)
    return MainMenu()

def CreateDirObject(name, key, thumb=R(ICON), art=R(ART), summary=None):
    myDir         = DirectoryObject()
    myDir.title   = name
    myDir.key     = key
    myDir.summary = summary
    myDir.thumb   = thumb
    myDir.art     = art
    return myDir
