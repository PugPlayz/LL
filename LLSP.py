import requests,re,threading,time,os,ujson,os.path, getpass, admin, winreg, ctypes, sys
from os import system
from playsound import playsound
from datetime import date
from datetime import datetime, timedelta



def create_key(name: str="default", path: ""=str)->bool:
    reg_key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_WRITE) 
    if not reg_key:
        return False

    winreg.SetValueEx(reg_key,name,0,winreg.REG_SZ,path)
    reg_key.Close()
    return True

if create_key("LazyLeaguer", r"{}".format(os.path.abspath(__file__))):
    print("Added startup key.")
else:
    print("Failed to add startup key.")
        
if os.path.isfile("./settings.json"):
    with open("settings.json", "r") as settings:
        settings = ujson.load(settings)
        api_key = settings['api-key']
        logPath = settings['logPath']
        soundPath = settings['soundPath']
        tTime = settings['Time']
else:
    settings = {}
    settings["api-key"] = "RGAPI-7a0f2e60-ad30-4242-a666-d58d63927e1c"
    settings["logPath"] = "C:\\Riot Games\\League of Legends\\Logs\\GameLogs"
    settings["soundPath"] = "./Alarm.mp3"
    settings["Time"] = 50
    tTime = settings["Time"]
    api_key = settings["api-key"]
    logPath = settings["logPath"]
    soundPath = settings["soundPath"]
    with open("settings.json", "w") as outfile:
        defaultDump = ujson.dump(settings,outfile,indent=4)


while True:
    dt = datetime.today()
    def Alert():
            print("Alert")
            time.sleep(tTime)
            global soundPath
            playsound(soundPath)
            time.sleep(60)

    def Request(pIGN, region):
        print("Request")
        l = 0
        a = 0
        while l == 0:
            try:
                a+=1
                print(a,'eSID Attempts')
                eSID = requests.get("https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}".format(region,pIGN,api_key),  timeout=10).json()
                if eSID["id"]:
                    iD = eSID["id"]
                    l+=1       
            except Exception as e:
                print(e)
            
        gT = 0
        a = 0
        while gT <= 0:
            try: 
                a+=1
                print(a,'gT Attempts')
                gT1 = requests.get("https://{}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{}?api_key={}".format(region,iD,api_key),  timeout=10).json()
                gT = gT1["gameStartTime"]
            except Exception as e:
                print(e)
        Alert()
        
    def SearchLog(logPathDirect, item, api_key):
        print("SearchLog")
        a = 0
        while True:
            a+=1
            print(a, 'SearchLog Attempts')
            f = open("{}\{}_r3dlog.txt".format(logPathDirect,item))
            f = f.read()
            if "**LOCAL**" in f:
                region = re.findall("-PlatformID=....", f)
                region = str(region)
                region = region.replace("-PlatformID=", "")
                region = region.replace('"', "")
                region = region.strip("]['")
                print(region)
                pIGN = re.findall('...................LOCAL..', f)
                pIGN = str(pIGN)
                pIGN = re.split("\s", pIGN)
                if pIGN:
                    pIGN = pIGN[2]
                    Request(pIGN, region)
                    break
            time.sleep(1)
            
        

    def GetRecent(dt, time, logPath):
        print("GetRecent")
        fileTime = str(time.ctime(os.path.getmtime(logPath)))
        d = datetime.strptime(fileTime,"%a %b  %d %H:%M:%S %Y")
        delta = timedelta(minutes=1)
        time = dt - d
        if dt < d + delta:
            print("New Game Found")
            dirs = os.listdir(logPath)
            if len(dirs) > 1:
                for item in dirs:
                    tem = str(item)
                    date = item[0:10]
                    time = item[11:19]
                    d = datetime.strptime(item,"%Y-%m-%dT%H-%M-%S")
                    delta = timedelta(minutes=1)
                    if dt < d + delta:
                        logPathDirect = "{}\{}".format(logPath, item)
                        SearchLog(logPathDirect, item, api_key)
        else:
            print("too old of file")
    time.sleep(1)
    GetRecent(dt, time, logPath)






